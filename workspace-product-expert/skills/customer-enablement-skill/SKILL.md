---
name: customer-enablement-skill
description: "生成客户资料包、一页纸摘要、管理层材料、技术评审材料、采购确认材料、FAQ、ROI 一页纸和讲解脚本。Use after a proposal is reviewed and before customer acknowledgement."
---

# 客户赋能材料

## Inputs

- 已审核方案或内部预览方案。
- ROI 测算报告、收益口径和审核状态。
- 配置清单、技术边界、交付边界、认证文件。
- 客户画像、客户角色、客户反馈和异议。
- 当前客户承认状态。

## Input Sources

1. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取方案状态、客户承认状态、配置清单和交付边界。
2. 从 `../../data/document_library.json` 定位方案书、认证文件、客户确认页和已有赋能材料。
3. 储能项目从 `../../data/roi_measurement.json` 读取 ROI 测算结果和审核状态。
4. 从 `../../data/customer_profile.json` 读取客户画像、角色和决策链。
5. 从 `../../data/enablement_records.json` 读取客户查看、反馈、承认推进和历史异议。
6. 从 `../../data/faq_records.json` 读取已确认 FAQ 和待专家确认问题。
7. 方案未审核或 ROI 未审核时只能生成内部预览材料。

## Procedure

1. 按受众拆分材料：管理层、技术评审、采购确认、储能投资评审。
2. 生成一页纸方案摘要、管理层材料、技术评审材料、采购确认材料。
3. 储能项目生成 ROI 一页纸，但未审核 ROI 不得外发。
4. 生成客户 FAQ、方案讲解脚本和客户反馈表。
5. 根据反馈状态输出下一步推进动作。
6. 客户反馈必须回流方案工程，不直接改正式方案。

## Outputs

- 客户资料包目录。
- 一页纸方案摘要。
- 管理层材料。
- 技术评审材料。
- 采购确认材料。
- 储能 ROI 一页纸。
- 客户 FAQ。
- 方案讲解脚本。
- 客户反馈表。
- 客户承认状态建议。
- `writeback_plan`：目标表 `enablement_records`、`solution_master`、`document_library`，登记赋能材料、反馈、异议和客户承认状态；承认状态只有人工或客户明确确认后才可更新为已承认。

## Error Handling

- 方案未审核时只生成内部预览。
- ROI 未审核时 ROI 一页纸不可外发。
- 客户问题无依据时标记为待专家确认。
