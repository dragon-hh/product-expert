---
name: customer-profile-skill
description: "从本地 GDP 和飞书/客户导入数据读取客户画像、历史方案、历史订单、行业、区域和类似案例。Use when a demand record needs customer context, account history, opportunity/order context, or profile summary before solution work."
---

# 客户画像补全

## Inputs

- 客户名称、客户 ID、商机 ID 或历史订单 ID。
- 本地 GDP 客户画像数据：行业、区域、等级、规模、联系人、决策链。
- 历史需求、历史方案、历史订单、服务记录、ROI 测算记录。
- 相似客户、相似项目或同区域行业信息。

## Input Sources

1. 如提供 `customer_id` 或客户名称，从 `../../data/customer_profile.json` 读取客户画像。
2. 从 `../../data/demand_master.json` 读取历史需求。
3. 从 `../../data/solution_master.json` 读取历史方案。
4. 从 `../../data/order_master.json` 读取历史商机和订单。
5. 从 `../../data/service_records.json` 读取历史服务、故障和 FAE 支持记录。
6. 从 `../../data/roi_measurement.json` 读取历史 ROI 测算记录。
7. 如果本地表为空，输出缺失数据源，不得编造客户画像。

## Procedure

1. 按客户 ID 精确匹配；没有 ID 时再按客户名称、别名、商机 ID 匹配。
2. 合并客户主数据、历史需求、方案、订单、服务和 ROI 记录。
3. 对记录按时间、来源可信度、审核状态排序。
4. 提取客户画像摘要：行业、区域、规模、等级、决策链、采购习惯、历史痛点。
5. 输出相似案例、历史风险、潜在机会和需要销售确认的问题。

## Outputs

- 客户画像摘要。
- 历史方案、订单、服务和 ROI 摘要。
- 相似客户或相似项目。
- 历史风险与当前机会。
- 待销售确认的问题。
- `writeback_plan`：目标表 `customer_profile`，写入客户画像候选、历史摘要和来源证据；飞书提取内容默认待确认。

## Error Handling

- 客户重名时输出候选列表，不强行合并。
- 本地 GDP 无客户记录且本次输入不足时返回 `missing_source_data`，列出缺失字段和建议导入来源。
- 历史记录冲突时保留冲突证据和来源时间。
