---
name: inbox-normalize-skill
description: "把客户导入、飞书聊天、会议纪要、附件文本、服务记录或运行数据整理成 workspace-product-expert/data/inbox/*.json。Use when raw business input needs to become normalized local GDP records before data-sync-skill runs."
---

# Inbox 归一化

## Inputs

- 原始业务输入：客户表单、飞书聊天、会议纪要、附件文本、服务记录、运行数据导出或人工补录。
- 来源信息：来源类型、消息/文档链接、时间、提交人、客户名称、项目名称。
- 目标业务阶段：需求、方案、ROI、客户赋能、交付、服务、FAQ、运行数据或复盘。

## Input Sources

1. 用户本次粘贴或上传的原始文本、表格、会议纪要或附件解析结果。
2. 已导出的飞书聊天、群问答、飞书表格、客户表单或服务单。
3. 本地 GDP：读取 `../../data/catalog.json`、各表 `schema` 和已有 `records` 做去重。
4. 编号规则：读取 `../../references/id-rules.md` 生成新记录候选主键。
5. 写回规则：读取 `../../references/writeback-contract.md` 判断审核状态和禁止覆盖规则。

## Procedure

1. 判断原始输入对应的目标表：需求、客户画像、方案、订单、ROI、赋能、交付、现场、文档、FAQ、服务或运行数据。
2. 按目标表 schema 抽取字段；无法确认的信息留空或标记 `unknown`，不得补事实。
3. 按 `id-rules.md` 为新记录生成候选主键；已有主键或可确定重复记录时优先复用。
4. 写入来源字段：`source`、`source_evidence`、`data_status`、`created_at`、`updated_at`。
5. 飞书聊天、会议纪要和附件解析默认标记为 `待确认`；人工确认数据才可标记为 `已确认`。
6. 输出 `data/inbox/YYYYMMDD-<source>-<topic>.json` 的归一化 JSON 内容。
7. 提醒后续运行 `data-sync-skill` 执行正式 upsert。

## Outputs

- 归一化 inbox JSON 内容。
- 建议文件路径。
- 表级记录数量。
- 去重判断和冲突清单。
- 缺失字段清单。
- `writeback_plan`：目标是 `data/inbox/*.json`，随后由 `data-sync-skill` 写入本地 GDP。

## Error Handling

- 无法判断目标表时，输出候选表和澄清问题，不生成 inbox 文件。
- 缺少客户名称、项目名称或来源证据时，记录只能标记为 `待确认`。
- 与已有记录冲突时，不合并、不覆盖，输出冲突清单。
- 缺少主键且无法按规则生成时，不进入 `records`，只输出补充要求。
