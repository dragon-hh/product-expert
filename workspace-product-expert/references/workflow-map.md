# 产品专家工作流地图

## 主链路

客户信息采集 -> 项目需求明确 -> 应用场景明确 -> 年度需求明确 -> 采购计划明确 -> 储能 ROI 测算 -> 客户需求与项目说明书 -> 标准 Word 技术方案书 -> 方案工程审核 -> 客户赋能 -> 客户承认 -> 报价/合同/订单 -> 交付实施 -> FAE 运维 -> 实际运行数据回流 -> ROI 模型校准 -> 管理复盘。

## Skill 编排建议

| 阶段 | Skill 链 |
| --- | --- |
| 数据接入 | inbox-normalize-skill -> data-sync-skill |
| 需求采集 | demand-intake-skill -> customer-profile-skill -> scenario-detect-skill -> storage-project-detect-skill -> demand-gate-skill |
| 需求说明书 | requirement-brief-skill |
| 方案工程 | solution-word-draft-skill -> standard-package-match-skill -> solution-risk-review-skill |
| 储能 ROI | storage-project-detect-skill -> home-storage-roi-skill 或 ci-storage-roi-skill -> solution-risk-review-skill |
| 客户赋能 | customer-enablement-skill -> faq-memory-skill |
| 交付运维 | delivery-handoff-skill -> fae-support-skill -> faq-memory-skill |
| 复盘校准 | roi-calibration-skill -> review-report-skill |

## 通用输出要求

每个 skill 输出：`status`、`evidence`、`result`、`missing_fields`、`risks`、`review_required`、`writeback_plan`。写回本地 GDP 时遵守 `writeback-contract.md`，不得覆盖人工审核结论。
