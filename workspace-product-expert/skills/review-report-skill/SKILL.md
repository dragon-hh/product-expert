---
name: review-report-skill
description: "生成需求、方案、客户赋能、订单转化、FAQ、ROI、模板标准包、交付服务的周报、月报、季报、年报和优化建议。Use for periodic business review crons or management reporting."
---

# 经营复盘报告

## Inputs

- 报告周期：周、月、季、年。
- 客户需求主表、方案主表、ROI 测算主表。
- 客户赋能状态、客户承认状态、订单转化数据。
- 交付数据、服务数据、FAQ 数据、实际运行数据。
- 数据窗口、统计口径、缺失数据说明。

## Input Sources

1. 需求指标来自 `../../data/demand_master.json`。
2. 方案指标来自 `../../data/solution_master.json`。
3. 订单转化指标来自 `../../data/order_master.json`。
4. ROI 指标来自 `../../data/roi_measurement.json` 和 `../../data/operation_data.json`。
5. 客户赋能和承认指标来自 `../../data/enablement_records.json`。
6. FAQ 指标来自 `../../data/faq_records.json` 和 `../../data/service_records.json`。
7. 交付服务指标来自 `../../data/delivery_project.json`、`../../data/site_survey.json` 和 `../../data/service_records.json`。
8. 模板和标准包指标来自 `../../data/template_usage.json` 和 `../../data/standard_package_usage.json`。
9. 若关键表 `records` 为空，报告必须披露缺失范围，不得输出确定性趋势结论。

## Procedure

1. 按 `../../references/report-templates.md` 选择周期模板。
2. 计算北极星指标：方案有效转化率、ROI 达标项目转化率。
3. 计算关键业务指标：需求完整率、退回率、方案提交率、模板复用率、ROI 覆盖率、客户承认率、订单转化率、FAQ 闭环率、ROI 偏差率等。
4. 输出趋势、异常、原因、建议和管理层决策事项。
5. 输出可沉淀的复盘结论候选，由 agent 层决定是否进入长期记忆。

## Outputs

- 需求准入看板。
- 方案总览看板。
- ROI 看板。
- 客户赋能看板。
- 转化漏斗。
- FAQ 看板。
- 失败原因分析。
- 实际收益偏差分析。
- 周/月/季/年周期报告。
- 优化建议清单。
- 复盘结论候选。
- `writeback_plan`：目标表 `document_library` 和 `memory/YYYY-MM-DD.md`，登记报告路径和复盘结论候选；长期记忆晋升必须保留人工确认状态。

## Error Handling

- 数据窗口不完整时披露缺失范围。
- 指标异常时标记待人工确认。
- 不要基于不完整数据输出确定性管理结论。
