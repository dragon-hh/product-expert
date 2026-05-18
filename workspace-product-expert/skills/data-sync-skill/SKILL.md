---
name: data-sync-skill
description: "把客户导入、飞书提取、附件解析、服务记录、ROI 和运行数据写入 workspace-product-expert/data/*.json 本地 GDP。Use when cron or an operator needs to populate or refresh product-expert data tables before business skills read them."
---

# 本地 GDP 数据同步

## Inputs

- 客户主动导入、飞书聊天/表格提取、附件解析、人工确认、FAE/服务记录、ROI 参数或运行数据。
- 放入 `../../data/inbox/*.json` 的归一化导入文件。
- 本地数据目录索引：`../../data/catalog.json`。
- 已由 `inbox-normalize-skill` 或人工整理好的主键、来源证据和审核状态。

## Input Sources

1. **归一化导入文件**：默认读取 `../../data/inbox/*.json`。
2. **飞书提取结果**：从聊天、群问答、会议纪要、表格或附件中提取后，先归一化为 inbox 格式。
3. **客户或人工导入**：客户表单、销售补录、方案工程确认、FAE 服务记录和运行数据导出，先归一化为 inbox 格式。
4. **本地 GDP 目录**：根据 `../../data/catalog.json` 找到目标表、主键和匹配字段。

归一化导出文件格式：

```json
{
  "source": "customer_upload|feishu_chat|feishu_sheet|attachment_extract|manual_confirmed|service_record|ems_export|skill_output",
  "records": {
    "demand_master": [],
    "solution_master": [],
    "order_master": [],
    "faq_records": []
  }
}
```

`records` 的 key 必须对应 `catalog.json` 中的 source key。

## Procedure

1. 检查 `../../data/catalog.json` 是否存在且可解析。
2. 收集 `../../data/inbox/*.json` 中的归一化导入数据。
3. 对每个表按 catalog 中的 `primary_key` upsert 到本地 GDP 对应 `data/*.json` 的 `records`。
4. 每条写入记录必须保留来源字段：`_source`、`_synced_at`、`_sync_run_id`。
5. 写入 `../../data/sync_runs.json`，记录同步开始时间、结束时间、来源、写入数量、跳过数量和错误。
6. 输出同步摘要、失败数据源、字段缺失和待人工处理事项。

## Outputs

- 同步运行摘要。
- 各表写入数量、更新数量、跳过数量。
- 缺失主键或无法归一化的数据清单。
- 失败数据源和重试建议。
- `sync_runs.json` 记录编号。

## Error Handling

- `../../data/inbox` 没有可处理 JSON 文件时，返回 `no_input_data`。
- 导出文件 JSON 无法解析时，跳过该文件并记录错误。
- 表名不在 `catalog.json` 中时，跳过该表并记录错误。
- 记录缺少主键时，跳过该记录；不得凭空生成业务主键。新记录主键应在 `inbox-normalize-skill` 中按 `../../references/id-rules.md` 生成。
- 同步任务只写本地 GDP，不覆盖人工审核结论字段，除非来源数据明确携带更新后的审核状态。
