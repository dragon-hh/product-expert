#!/usr/bin/env python3
"""Upsert normalized product-expert exports into workspace data JSON tables."""
import argparse
import datetime as dt
import json
import sys
import uuid
from pathlib import Path


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def now_iso():
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def normalize_payload(payload):
    if isinstance(payload.get("records"), dict):
        return payload.get("source", "unknown"), payload["records"]
    tables = {k: v for k, v in payload.items() if isinstance(v, list)}
    return payload.get("source", "unknown"), tables


def upsert_records(table_path, primary_key, records, source, run_id, synced_at):
    table = load_json(table_path) if table_path.exists() else {"primary_key": primary_key, "records": []}
    existing = table.setdefault("records", [])
    index = {row.get(primary_key): i for i, row in enumerate(existing) if isinstance(row, dict) and row.get(primary_key)}
    inserted = updated = skipped = 0
    errors = []
    for row in records:
        if not isinstance(row, dict):
            skipped += 1
            errors.append({"reason": "record_not_object", "record": row})
            continue
        key = row.get(primary_key)
        if not key:
            skipped += 1
            errors.append({"reason": "missing_primary_key", "primary_key": primary_key, "record": row})
            continue
        enriched = dict(row)
        enriched["_source"] = source
        enriched["_synced_at"] = synced_at
        enriched["_sync_run_id"] = run_id
        if key in index:
            existing[index[key]].update(enriched)
            updated += 1
        else:
            existing.append(enriched)
            index[key] = len(existing) - 1
            inserted += 1
    save_json(table_path, table)
    return {"inserted": inserted, "updated": updated, "skipped": skipped, "errors": errors}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--inbox", default=None)
    parser.add_argument("--catalog", default=None)
    args = parser.parse_args()

    workspace = Path(args.workspace)
    catalog_path = Path(args.catalog) if args.catalog else workspace / "data" / "catalog.json"
    inbox = Path(args.inbox) if args.inbox else workspace / "data" / "inbox"
    run_id = str(uuid.uuid4())
    started_at = now_iso()
    summary = {
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": None,
        "status": "ok",
        "files": [],
        "tables": {},
        "errors": [],
    }

    if not catalog_path.exists():
        summary["status"] = "failed"
        summary["errors"].append({"reason": "missing_catalog", "path": str(catalog_path)})
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1

    catalog = load_json(catalog_path)
    sources = catalog.get("sources", {})
    files = sorted(inbox.glob("*.json")) if inbox.exists() else []
    if not files:
        summary["status"] = "no_input_data"
        summary["finished_at"] = now_iso()
        record_sync_run(workspace, summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    for file_path in files:
        file_result = {"path": str(file_path), "status": "ok", "tables": []}
        try:
            payload = load_json(file_path)
            source, tables = normalize_payload(payload)
        except Exception as exc:
            file_result["status"] = "failed"
            file_result["error"] = str(exc)
            summary["errors"].append({"file": str(file_path), "reason": "invalid_json", "error": str(exc)})
            summary["files"].append(file_result)
            continue

        for table_name, records in tables.items():
            if table_name not in sources:
                err = {"file": str(file_path), "table": table_name, "reason": "unknown_table"}
                summary["errors"].append(err)
                file_result["tables"].append({"table": table_name, "status": "skipped", "reason": "unknown_table"})
                continue
            if not isinstance(records, list):
                err = {"file": str(file_path), "table": table_name, "reason": "records_not_list"}
                summary["errors"].append(err)
                file_result["tables"].append({"table": table_name, "status": "skipped", "reason": "records_not_list"})
                continue
            meta = sources[table_name]
            table_path = workspace.parent / meta["path"] if meta["path"].startswith("workspace-product-expert/") else workspace / meta["path"]
            result = upsert_records(table_path, meta["primary_key"], records, source, run_id, started_at)
            summary["tables"].setdefault(table_name, {"inserted": 0, "updated": 0, "skipped": 0})
            for key in ["inserted", "updated", "skipped"]:
                summary["tables"][table_name][key] += result[key]
            for err in result["errors"]:
                err["table"] = table_name
                err["file"] = str(file_path)
                summary["errors"].append(err)
            file_result["tables"].append({"table": table_name, **result, "errors": result["errors"][:5]})
        summary["files"].append(file_result)

    if summary["errors"]:
        summary["status"] = "completed_with_errors"
    summary["finished_at"] = now_iso()
    record_sync_run(workspace, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def record_sync_run(workspace, summary):
    table_path = workspace / "data" / "sync_runs.json"
    table = load_json(table_path) if table_path.exists() else {"primary_key": "run_id", "records": []}
    records = table.setdefault("records", [])
    records.append({
        "run_id": summary["run_id"],
        "started_at": summary["started_at"],
        "finished_at": summary["finished_at"],
        "status": summary["status"],
        "source": "inbox",
        "files": [item.get("path") for item in summary.get("files", [])],
        "tables": summary["tables"],
        "error_count": len(summary["errors"]),
        "errors": summary["errors"][:50],
    })
    save_json(table_path, table)


if __name__ == "__main__":
    sys.exit(main())
