# 本地 GDP 编号规则

本地 GDP 新记录必须有主键。`data-sync-skill` 只负责 upsert，不为缺少主键的记录自动造号。客户导入、飞书提取、附件解析和 skill 输出在进入 `data/inbox/*.json` 前，应按本规则生成候选主键。

## 编号格式

| 表 | 主键 | 格式 |
| --- | --- | --- |
| `customer_profile` | `customer_id` | `CUST-YYYYMMDD-NNN` |
| `demand_master` | `demand_id` | `D-YYYYMMDD-NNN` |
| `solution_master` | `solution_id` | `S-YYYYMMDD-NNN` |
| `order_master` | `order_id` | `O-YYYYMMDD-NNN` |
| `delivery_project` | `delivery_id` | `DEL-YYYYMMDD-NNN` |
| `site_survey` | `survey_id` | `SUR-YYYYMMDD-NNN` |
| `document_library` | `document_id` | `DOC-YYYYMMDD-NNN` |
| `roi_measurement` | `roi_id` | `ROI-YYYYMMDD-NNN` |
| `roi_parameter` | `parameter_id` | `PAR-YYYYMMDD-NNN` |
| `enablement_records` | `enablement_id` | `ENB-YYYYMMDD-NNN` |
| `faq_records` | `faq_id` | `FAQ-YYYYMMDD-NNN` |
| `service_records` | `service_id` | `SRV-YYYYMMDD-NNN` |
| `operation_data` | `operation_id` | `OP-YYYYMMDD-NNN` |
| `template_usage` | `usage_id` | `TU-YYYYMMDD-NNN` |
| `standard_package_usage` | `usage_id` | `SPU-YYYYMMDD-NNN` |

`NNN` 从当天同类记录的最大序号加 1。无法确认是否重复时，先输出候选记录和去重建议，不写入正式表。

## 去重优先级

1. 已有主键完全匹配。
2. 客户名称 + 项目名称 + 业务阶段匹配。
3. 来源消息 ID、文档路径或附件 hash 匹配。
4. 文本相似但证据不足时，标记为 `待确认`，不得静默合并。

## 来源字段

新记录至少保留：

- `source` 或 `_source`
- `source_evidence`
- `data_status`
- `created_at`
- `updated_at`

飞书聊天、会议纪要和附件解析默认 `data_status=待确认`。人工表单或明确审核记录可以写 `data_status=已确认` 或对应审核状态。
