---
name: demand-gate-skill
description: "计算需求完整度评分，识别硬性缺失项，生成澄清问题和方案生成准入状态。Use when deciding whether a demand may enter solution engineering, draft-only mode, clarification mode, or sales return mode."
---

# 需求准入门禁

## Inputs

- Demand Record JSON。
- 储能识别结果：是否储能、储能类型、ROI 数据完整度。
- 风险与限制：认证、交期、预算、现场条件、竞品、交付边界。
- 需求说明书状态：未生成、草稿、已确认。

## Input Sources

1. 用户直接提供 Demand Record JSON 时，以本次输入为准。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取客户需求记录。
3. 储能项目的 ROI 准入状态可从 `../../data/roi_measurement.json` 按 `demand_id`、`solution_id`、客户名称或项目名称读取。
4. 需求说明书状态可从 `../../data/document_library.json` 读取 `document_type=需求说明书` 的记录。
5. 如果需求主表为空且用户没有提供 Demand Record JSON，返回 `blocked`。

## Procedure

1. 检查硬性门禁：客户信息、项目需求、应用场景、年度需求、采购计划、储能 ROI 前置数据、需求说明书。
2. 使用 `scripts/score_demand.py` 计算基础完整度评分。
3. 按固定权重解释评分：客户信息 15%、项目需求 20%、应用场景 20%、年度需求 15%、采购计划 15%、风险限制 10%。
4. 储能项目按 ROI 数据完整度追加门禁：不足 30% 阻断，30%-59% 只澄清，60%-84% 只允许初稿，85% 以上进入审核。
5. 按阈值输出动作：90+ 正式方案、75-89 初稿待确认、60-74 澄清清单、60 以下退回销售。
6. 为销售生成补充问题，为方案工程师生成风险提示。

## Outputs

- 准入结论。
- 完整度评分和分项评分。
- 硬性缺失字段。
- 需求澄清清单。
- 方案生成允许状态。
- 方案工程风险提示。
- 审核角色建议。
- `writeback_plan`：目标表 `demand_master`，更新 `demand_completeness_score`、`allow_solution_generation`、`missing_information`、`review_status`，不得覆盖人工审核结论。

## Error Handling

- Demand Record JSON 无法解析时返回 `failed`。
- 缺少客户名称、项目背景、应用场景、年度需求或采购计划时，不允许正式方案。
- 储能 ROI 关键字段不足时，不允许正式投资回报结论。
- 评分证据不足时返回 `needs_review`，并列出缺少的证据。
