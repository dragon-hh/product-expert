---
name: scenario-detect-skill
description: "判断新建、替换、扩容、改造、集成、试点、投标、年度框架等应用场景并输出置信度和证据。Use when a demand or project description needs scenario labels before standard package matching."
---

# 应用场景识别

## Inputs

- 项目描述、客户痛点、建设目标。
- 现网情况：是否已有系统、是否替换竞品、是否扩容或改造。
- 商务场景：试点、投标、年度框架、集成合作。
- 技术线索：接口、协议、部署范围、容量变化、认证要求。

## Input Sources

1. 用户本次输入的项目描述和客户需求文本。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取项目背景、痛点、目标和范围。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取既有方案类型和应用场景。
4. 如提供文档编号，从 `../../data/document_library.json` 读取需求说明书或方案附件。
5. 如果没有任何项目描述、需求记录或方案记录，返回 `needs_sales_input`。

## Procedure

1. 识别场景关键词和业务意图。
2. 从新建、替换、扩容、改造、集成、试点、投标、年度框架中选择一个 primary 场景。
3. 可输出多个 secondary 场景，但必须说明证据。
4. 为每个场景给置信度、证据句和澄清问题。
5. 场景为 unknown 时，明确阻止标准包匹配。

## Outputs

- primary_scenario。
- secondary_scenarios。
- confidence。
- evidence。
- clarification_questions。
- standard_package_allowed。
- `writeback_plan`：目标表 `demand_master`，更新 `application_scenario`、`scenario_confidence`、`scenario_evidence`；证据不足时只写候选。

## Error Handling

- 多个场景冲突时输出候选优先级和冲突原因。
- 证据不足时返回 `needs_sales_input`。
- 场景不可确认时不得强行匹配标准包。
