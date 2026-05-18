---
name: requirement-brief-skill
description: "生成《客户需求与项目说明书》，作为方案工程和正式 Word 技术方案书的唯一前置依据。Use after demand intake and demand gate when a structured requirement brief is needed."
---

# 需求说明书生成

## Inputs

- 已结构化的客户需求记录。
- 客户画像摘要。
- 需求完整度评分和准入结论。
- 场景识别结果、年度需求、采购计划。
- 储能 ROI 前置信息、竞品信息、风险与限制。

## Input Sources

1. 用户本次输入的客户需求记录和准入结论。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取需求记录。
3. 如提供客户名称或 `customer_id`，从 `../../data/customer_profile.json` 读取客户画像。
4. 储能项目从 `../../data/roi_measurement.json` 读取 ROI 前置状态或既有测算。
5. 从 `../../data/document_library.json` 检查是否已有需求说明书，避免重复生成。
6. 如果需求记录为空或准入分数不足，只输出澄清说明。

## Procedure

1. 确认需求准入结论是否允许生成说明书。
2. 按 15 节结构生成说明书：客户基本信息、客户画像、项目背景、业务痛点、建设目标、项目范围、应用场景、年度需求、采购计划、技术需求、认证与交付要求、储能 ROI 前置信息、风险与限制、待补充问题、准入结论。
3. 对待补充问题做显著标记，不得隐藏在正文里。
4. 明确说明是否满足方案生成条件。
5. 输出正文、摘要和后续方案工程输入字段。

## Outputs

- 《客户需求与项目说明书》正文。
- 待补充问题清单。
- 方案生成建议。
- 准入结论。
- 后续 Word 方案书输入摘要。
- `writeback_plan`：目标表 `document_library` 和 `demand_master`，登记需求说明书路径并更新 `demand_brief_path`；正式版必须保留审核状态。

## Error Handling

- 评分低于 60 时只输出澄清说明，不生成正式说明书。
- 75-89 分必须标记待确认项。
- 储能 ROI 前置不足时不得给正式投资结论。
