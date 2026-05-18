#!/usr/bin/env python3
"""Calculate a baseline home-storage ROI from JSON input."""
import json
import sys
from pathlib import Path


def npv(rate, cashflows):
    return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cashflows))


def irr(cashflows):
    low, high = -0.95, 1.0
    for _ in range(100):
        mid = (low + high) / 2
        value = npv(mid, cashflows)
        if abs(value) < 1e-7:
            return mid
        if value > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def payback(cashflows):
    total = 0.0
    for year, cf in enumerate(cashflows[1:], start=1):
        prev = total
        total += cf
        if total >= -cashflows[0]:
            return year - 1 + ((-cashflows[0] - prev) / cf if cf else 0)
    return None


def number(data, key, default=0.0):
    try:
        return float(data.get(key, default) or default)
    except (TypeError, ValueError):
        return default


REQUIRED_FOR_FORMAL = [
    "project_total_investment", "annual_pv_generation_kwh", "self_use_rate_without_storage",
    "self_use_rate_with_storage", "resident_purchase_price", "feed_in_tariff",
    "annual_discharge_kwh", "peak_valley_spread",
]


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")) if len(sys.argv) > 1 else json.load(sys.stdin)
    missing = [key for key in REQUIRED_FOR_FORMAL if data.get(key) in (None, "", [])]
    capex = number(data, "project_total_investment")
    pv_generation = number(data, "annual_pv_generation_kwh")
    self_before = number(data, "self_use_rate_without_storage")
    self_after = number(data, "self_use_rate_with_storage")
    purchase_price = number(data, "resident_purchase_price")
    feed_in = number(data, "feed_in_tariff")
    annual_discharge = number(data, "annual_discharge_kwh")
    spread = number(data, "peak_valley_spread")
    efficiency = number(data, "system_efficiency", 0.9)
    subsidy = number(data, "subsidy_annual")
    vpp = number(data, "vpp_annual")
    om = number(data, "annual_om_cost")
    discount = number(data, "discount_rate", 0.08)
    life = int(number(data, "life_years", 10))
    degradation = number(data, "annual_degradation_rate", 0.02)
    self_use_uplift = max(0.0, pv_generation * max(0.0, self_after - self_before) * max(0.0, purchase_price - feed_in))
    arbitrage = max(0.0, annual_discharge * spread * efficiency)
    conservative = self_use_uplift + arbitrage
    basic = conservative + subsidy
    value_added = vpp
    gross = basic + value_added
    net_year_1 = gross - om
    cashflows = [-capex] + [net_year_1 * ((1 - degradation) ** year) for year in range(life)]
    static_payback = capex / net_year_1 if capex > 0 and net_year_1 > 0 else None
    dynamic_payback = payback(cashflows) if capex > 0 else None
    result_irr = irr(cashflows) if capex > 0 and any(cf > 0 for cf in cashflows[1:]) else None
    roi = net_year_1 / capex if capex > 0 else None
    recommendation = "recommended" if static_payback and static_payback <= 6 else "cautious" if static_payback and static_payback <= 9 else "not_recommended_or_needs_more_data"
    print(json.dumps({
        "status": "success" if not missing else "needs_more_data",
        "can_publish_formal": not missing,
        "missing_fields": missing,
        "revenue": {
            "pv_self_use_uplift": round(self_use_uplift, 2),
            "peak_valley_arbitrage": round(arbitrage, 2),
            "conservative_revenue": round(conservative, 2),
            "basic_revenue": round(basic, 2),
            "value_added_revenue": round(value_added, 2),
            "annual_gross_revenue": round(gross, 2),
            "annual_net_revenue_year_1": round(net_year_1, 2),
        },
        "metrics": {
            "project_total_investment": round(capex, 2),
            "static_payback_years": None if static_payback is None else round(static_payback, 2),
            "dynamic_payback_years": None if dynamic_payback is None else round(dynamic_payback, 2),
            "roi_year_1": None if roi is None else round(roi, 4),
            "irr": None if result_irr is None else round(result_irr, 4),
            "npv": round(npv(discount, cashflows), 2),
        },
        "recommendation": recommendation,
        "review_required": "ROI owner and solution engineer",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
