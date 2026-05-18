---
name: demand-intake-skill
description: "采集和结构化客户、项目、场景、年度需求、采购计划。Use when sales input, meeting notes, Feishu messages, or rough customer requirements need to become a standard demand record, missing-field list, interview outline, and solution application."
---

# 需求采集结构化

## Inputs

- 销售原始输入：飞书消息、会议纪要、电话纪要、客户邮件、表单或手工粘贴文本。
- 客户基础信息：客户名称、行业、区域、规模、等级、联系人、决策链。
- 项目信息：项目名称、背景、痛点、目标、范围、功能需求、技术需求、认证要求、周期。
- 年度和采购信息：年度采购规模、分阶段计划、覆盖区域、产品线、预算、报价节点、合同节点。
- 已知风险：竞品、交期、认证、预算、现场条件、交付边界、合规限制。

## Input Sources

1. 用户本次输入是主来源：聊天记录、会议纪要、客户邮件、表单或手工粘贴文本。
2. 如提供 `customer_id` 或客户名称，可从 `../../data/customer_profile.json` 补充客户画像候选。
3. 如提供 `demand_id`，可从 `../../data/demand_master.json` 读取既有需求记录，避免重复建档。
4. 如提供文档编号或附件路径，可从 `../../data/document_library.json` 找到会议纪要、需求说明或方案附件。
5. 本 skill 输出的结构化记录按 `../../references/writeback-contract.md` 写回本地 GDP 的 `demand_master` 候选记录。
6. 如果本地表 `records` 为空，只使用用户本次输入，不得伪造历史画像或历史需求。

## Procedure

1. 抽取客户、项目、年度需求、采购计划、风险和限制字段。
2. 按 `../../references/data-contracts.md` 的 Demand Record JSON 结构输出字段。
3. 对无法确认的信息写 `unknown`，不要替销售补事实。
4. 识别字段冲突，例如客户预算状态与采购节点不一致、项目目标与应用场景不一致。
5. 生成客户访谈提纲，问题必须对应缺失字段。
6. 输出方案申请单草稿，标记是否可进入需求准入评分。

## Outputs

- 客户需求记录 JSON。
- 缺失字段清单。
- 字段冲突清单。
- 客户访谈提纲。
- 方案申请单草稿。
- 下一步建议：补充信息、客户画像补全、场景识别、储能识别或需求准入。
- `writeback_plan`：目标表 `demand_master`，主键 `demand_id`，写入字段、来源证据、数据状态和禁止覆盖说明。

## Error Handling

- 客户名称和项目背景都缺失时，状态为 `blocked`，只输出补采问题。
- 输入互相矛盾时，状态为 `needs_sales_input`，列出冲突字段和待确认问题。
- 来源不可靠或只有单句线索时，状态为 `draft_lead`，不得生成方案申请结论。
