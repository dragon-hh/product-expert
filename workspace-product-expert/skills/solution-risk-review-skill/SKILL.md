---
name: solution-risk-review-skill
description: "检查技术、认证、交付、商务、ROI、竞品和外发风险，输出风险等级和审核角色建议。Use before any proposal, ROI result, competitor comparison, or customer-facing material is sent externally."
---

# 方案风险审核

## Inputs

- 方案 Word 初稿、客户赋能材料或 ROI 报告。
- 产品标准配置、技术协议、认证文件。
- 交付边界、验收标准、交付周期。
- ROI 测算报告、收益口径、假设和审核状态。
- 竞品信息、商务承诺、价格或合同相关表述。

## Input Sources

1. 用户本次输入的方案文本、ROI 报告或客户外发材料。
2. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取方案状态、配置、边界和附件。
3. 从 `../../data/document_library.json` 定位方案书、认证文件、客户确认页和合同附件。
4. 从 `../../data/roi_measurement.json` 读取 ROI 假设、收益口径和审核状态。
5. 从 `../../data/standard_package_usage.json` 读取标准包匹配结果和审核状态。
6. 从 `../../data/order_master.json` 读取订单、报价或合同节点相关风险。
7. 缺少外发材料或方案正文时返回 `blocked`。

## Procedure

1. 扫描没有证据来源的技术参数、认证、交期、成本、价格、竞品和合同承诺。
2. 检查 ROI 假设、收益口径、敏感性和审核状态。
3. 检查外发材料是否标注审核角色、审核状态和待确认项。
4. 按低、中、高分级风险。
5. 给出审核角色建议、修改建议和外发控制建议。

## Outputs

- 风险提示清单。
- 风险等级。
- 审核角色建议。
- 待确认事项。
- 外发控制建议。
- 可修订文本建议。
- `writeback_plan`：目标表 `solution_master` 和 `document_library`，更新 `risk_level`、`risk_review_result`、`pending_review_items` 并登记风险报告；不得把建议改成正式审核结论。

## Error Handling

- 关键证据缺失时标记高风险或 `needs_review`。
- 客户外发材料无审核状态时返回 `blocked`。
- ROI 正式结果无审核时返回 `blocked`。
