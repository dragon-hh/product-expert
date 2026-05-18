#!/usr/bin/env python3
"""Score a product-expert demand record from JSON."""
import json
import sys
from pathlib import Path

WEIGHTS = {
    "customer_info": 15,
    "project_need": 20,
    "scenario": 20,
    "annual_demand": 15,
    "procurement_plan": 15,
    "risks_constraints": 10,
}
FIELDS = {
    "customer_info": ["customer.name", "customer.industry", "customer.region", "customer.scale", "customer.contacts"],
    "project_need": ["project.background", "project.pain_points", "project.goals", "project.scope", "project.technical_requirements"],
    "scenario": ["scenario.primary"],
    "annual_demand": ["annual_demand.total", "annual_demand.phase_plan", "annual_demand.product_lines"],
    "procurement_plan": ["procurement_plan.timeline", "procurement_plan.method", "procurement_plan.budget_status", "procurement_plan.quote_node", "procurement_plan.contract_node"],
    "risks_constraints": ["risks", "constraints"],
}
HARD_GATES = ["customer.name", "project.background", "scenario.primary", "annual_demand.total", "procurement_plan.timeline"]


def get(data, path):
    cur = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def present(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().lower() not in {"unknown", "n/a", "none", "未知"}
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


def decide(score):
    if score >= 90:
        return "allow_formal_solution"
    if score >= 75:
        return "allow_draft_with_pending_items"
    if score >= 60:
        return "clarification_only"
    return "return_to_sales"


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")) if len(sys.argv) > 1 else json.load(sys.stdin)
    groups, missing, weighted = {}, [], 0.0
    for group, fields in FIELDS.items():
        hits = [field for field in fields if present(get(data, field))]
        ratio = len(hits) / len(fields)
        groups[group] = {
            "completion": round(ratio, 4),
            "score": round(ratio * WEIGHTS[group], 2),
            "missing": [field for field in fields if field not in hits],
        }
        missing.extend(groups[group]["missing"])
        weighted += ratio * WEIGHTS[group]
    base_score = round(weighted * 100 / sum(WEIGHTS.values()), 2)
    hard_missing = [field for field in HARD_GATES if not present(get(data, field))]
    storage = data.get("storage", {}) if isinstance(data.get("storage"), dict) else {}
    is_storage = bool(storage.get("is_storage_project"))
    try:
        roi_completion = float(storage.get("roi_data_completeness") or 0.0)
    except (TypeError, ValueError):
        roi_completion = 0.0
    final_score, roi_gate = base_score, "not_storage"
    if is_storage:
        if roi_completion < 0.3:
            final_score, roi_gate = min(final_score, 59.0), "roi_blocked"
        elif roi_completion < 0.6:
            final_score, roi_gate = min(final_score, 74.0), "roi_clarification_only"
        elif roi_completion < 0.85:
            final_score, roi_gate = min(final_score, 89.0), "roi_draft_only"
        else:
            roi_gate = "roi_ready_for_review"
    if hard_missing and final_score >= 75:
        final_score = min(final_score, 74.0)
    print(json.dumps({
        "status": "success",
        "score": round(final_score, 2),
        "base_score_without_roi_gate": base_score,
        "decision": decide(final_score),
        "groups": groups,
        "missing_fields": sorted(set(missing)),
        "hard_gate_missing": hard_missing,
        "storage_roi_gate": roi_gate,
        "review_required": final_score >= 75,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
