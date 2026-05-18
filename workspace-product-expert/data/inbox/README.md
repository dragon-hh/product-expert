# data/inbox

这里存放准备写入本地 GDP 的归一化 JSON 文件。客户主动导入、飞书聊天/表格提取、附件解析、服务记录和运行数据导出，应先由 `inbox-normalize-skill` 整理成此目录下的文件，再由 `data-sync-skill` 写入 `workspace-product-expert/data/*.json`。

## 基本格式

```json
{
  "source": "customer_upload|feishu_chat|feishu_sheet|attachment_extract|manual_confirmed|service_record|ems_export|skill_output",
  "records": {
    "demand_master": [],
    "faq_records": []
  }
}
```

`records` 的 key 必须匹配 `../catalog.json` 的 source key。每条记录必须带目标表主键；新记录按 `../../references/id-rules.md` 生成候选主键。

飞书聊天、会议纪要和附件解析默认是候选事实，应带 `data_status=待确认` 和 `source_evidence`。
