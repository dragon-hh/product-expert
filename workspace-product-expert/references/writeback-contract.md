# 写回契约

## 核心口径

`workspace-product-expert/data/` 是本项目 GDP。skill 可以生成结构化结果、候选记录和报告，但写回本地 GDP 时必须带上目标表、主键、来源证据、审核状态和禁止覆盖规则。

## 写入入口

1. 批量导入或飞书提取结果：先写成 `data/inbox/*.json` 的归一化导入文件，再由 `data-sync-skill` upsert 到本地 GDP。
2. skill 运行中的确定性结果：输出 `writeback_plan`，说明目标表和字段；只有用户、cron 或上层 agent 明确执行写回时才更新 `data/*.json`。
3. 人工审核结论：可以更新审核状态；未经人工确认的模型推断只能写成候选、待确认或建议字段。

每条写回记录至少保留：`source` 或 `_source`、来源证据、创建/更新时间、审核状态。通过同步脚本写入时自动增加 `_source`、`_synced_at`、`_sync_run_id`。

新记录主键按 `id-rules.md` 生成。`data-sync-skill` 不为缺主键记录自动造号；缺主键记录会被跳过。

## 禁止覆盖

- 不覆盖 `已审核`、`已承认`、`可外发`、`人工确认` 等人工结论，除非新来源明确携带更新后的人工审核状态。
- 飞书聊天提取内容默认是候选事实，不直接变成已确认事实。
- ROI、认证、技术参数、交付周期、合同承诺必须保留审核角色。
- 冲突数据不静默覆盖，写入 `pending_review_items`、`missing_information`、`objections` 或报告待确认事项。

## Skill 写回目标

| Skill | 主要写回表 | 写回内容 |
| --- | --- | --- |
| `inbox-normalize-skill` | `data/inbox/*.json` | 将客户导入、飞书提取、附件解析、服务记录或运行数据整理成可同步 JSON |
| `data-sync-skill` | 所有 `data/*.json`、`sync_runs.json` | 将 `data/inbox/*.json` 归一化记录 upsert 到本地 GDP，并记录同步批次 |
| `demand-intake-skill` | `demand_master.json` | 新需求记录、缺失字段、来源证据、数据状态 |
| `customer-profile-skill` | `customer_profile.json` | 客户画像候选、历史需求/方案/订单/服务摘要 |
| `scenario-detect-skill` | `demand_master.json` | `application_scenario`、`scenario_confidence`、`scenario_evidence` |
| `storage-project-detect-skill` | `demand_master.json` | `is_storage_project`、`storage_project_type`、`roi_data_completeness` |
| `demand-gate-skill` | `demand_master.json` | `demand_completeness_score`、`allow_solution_generation`、`missing_information`、`review_status` |
| `requirement-brief-skill` | `document_library.json`、`demand_master.json` | 需求说明书文档索引、`demand_brief_path` |
| `home-storage-roi-skill` | `roi_measurement.json`、`solution_master.json` | 户储 ROI 测算记录、ROI 版本、审核状态、方案 ROI 关联 |
| `ci-storage-roi-skill` | `roi_measurement.json`、`solution_master.json` | 工商储 ROI 测算记录、ROI 版本、审核状态、方案 ROI 关联 |
| `solution-word-draft-skill` | `solution_master.json`、`document_library.json`、`template_usage.json` | 方案草稿、方案附件索引、模板使用记录 |
| `standard-package-match-skill` | `standard_package_usage.json`、`solution_master.json` | 标准包匹配结果、复用状态、审核状态 |
| `solution-risk-review-skill` | `solution_master.json`、`document_library.json` | 风险等级、风险审核结果、待确认事项、风险报告索引 |
| `customer-enablement-skill` | `enablement_records.json`、`solution_master.json`、`document_library.json` | 赋能材料、客户反馈、异议、客户承认状态建议或确认状态 |
| `delivery-handoff-skill` | `delivery_project.json`、`document_library.json`、`site_survey.json` | 交付 9 件套、交付边界、验收要求、现场条件和运行数据字段 |
| `fae-support-skill` | `service_records.json`、`faq_records.json` | 服务记录、专家转接、FAQ 候选 |
| `faq-memory-skill` | `faq_records.json`、`memory/YYYY-MM-DD.md` | FAQ 候选、专家修正、知识库更新候选、可沉淀结论 |
| `roi-calibration-skill` | `roi_measurement.json`、`roi_parameter.json`、`document_library.json` | ROI 偏差、校准状态、参数修正候选、校准报告 |
| `review-report-skill` | `document_library.json`、`memory/YYYY-MM-DD.md` | 周/月/季/年报告索引、复盘结论候选 |

## `data/inbox` 归一化格式

```json
{
  "source": "customer_upload|feishu_chat|feishu_sheet|attachment_extract|manual_confirmed|service_record|ems_export|skill_output",
  "records": {
    "demand_master": [],
    "solution_master": [],
    "roi_measurement": []
  }
}
```

`records` 的 key 必须匹配 `data/catalog.json` 的 source key。缺主键的记录不得写入正式表。
