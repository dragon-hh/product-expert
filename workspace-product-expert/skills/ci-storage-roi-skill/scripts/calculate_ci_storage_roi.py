#!/usr/bin/env python3
"""Calculate a baseline commercial and industrial storage ROI from JSON input."""
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
    "project_total_investment", "daily_discharge_kwh", "peak_valley_spread",
    "annual_operating_days", "time_of_use_tariff_available", "load_curve_available",
]


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")) if len(sys.argv) > 1 else json.load(sys.stdin)
    missing = [key for key in REQUIRED_FOR_FORMAL if data.get(key) in (None, "", [], False)]
    capex = number(data, "project_total_investment")
    arbitrage = max(0.0, number(data, "daily_discharge_kwh") * number(data, "peak_valley_spread") * number(data, "system_efficiency", 0.88) * number(data, "annual_operating_days", 300))
    demand_savings = max(0.0, number(data, "demand_reduction_kw") * number(data, "demand_charge_per_kw_month") * 12)
    pv_consumption = max(0.0, number(data, "pv_extra_self_use_kwh") * max(0.0, number(data, "purchase_price") - number(data, "feed_in_tariff")))
    conservative = arbitrage + demand_savings + pv_consumption
    basic = conservative + number(data, "confirmed_subsidy_annual")
    value_added = number(data, "demand_response_annual") + number(data, "vpp_annual")
    gross = basic + value_added
    net_year_1 = gross - number(data, "annual_om_cost")
    discount = number(data, "discount_rate", 0.08)
    life = int(number(data, "life_years", 10))
    degradation = number(data, "annual_degradation_rate", 0.025)
    cashflows = [-capex] + [net_year_1 * ((1 - degradation) ** year) for year in range(life)]
    formal_allowed = not missing
    static_payback = capex / net_year_1 if capex > 0 and net_year_1 > 0 else None
    dynamic_payback = payback(cashflows) if formal_allowed and capex > 0 else None
    result_irr = irr(cashflows) if formal_allowed and capex > 0 and any(cf > 0 for cf in cashflows[1:]) else None
    roi = net_year_1 / capex if capex > 0 else None
    recommendation = "recommended" if static_payback and static_payback <= 5 else "cautious" if static_payback and static_payback <= 8 else "not_recommended_or_needs_more_data"
    print(json.dumps({
        "status": "success" if formal_allowed else "needs_more_data",
        "can_publish_formal": formal_allowed,
        "missing_fields": missing,
        "revenue": {
            "peak_valley_arbitrage": round(arbitrage, 2),
            "demand_management": round(demand_savings, 2),
            "pv_self_consumption_uplift": round(pv_consumption, 2),
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
            "npv": None if not formal_allowed else round(npv(discount, cashflows), 2),
        },
        "recommendation": recommendation,
        "review_required": "ROI owner and solution engineer",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
