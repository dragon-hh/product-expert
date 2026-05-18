# 产品专家 OpenClaw Agent 项目总览

## 项目定位

本项目交付一个 `product-expert` OpenClaw agent 工作流包，用于把客户从“模糊需求”推进到“可生成方案、可测算 ROI、可客户承认、可转订单、可交付、可复盘”的标准业务闭环。

当前核心资产：

- 工作区：`workspace-product-expert/`
- 本地 GDP：`workspace-product-expert/data/*.json`
- Skill 数量：19 个
- Cron 定时任务数量：11 个
- 心跳机制：1 套，定义于 `workspace-product-expert/HEARTBEAT.md`
- Cron 清单：`jobs.json`
- Skill 清单：`workspace-product-expert/skill-manifest.json`

## 运行时数据流

```text
客户导入 / 飞书聊天 / 飞书表格 / 会议纪要 / 附件解析 / 服务记录 / 运行数据
-> inbox-normalize-skill
-> workspace-product-expert/data/inbox/*.json
-> data-sync-skill
-> workspace-product-expert/data/*.json 本地 GDP
-> 业务 skill 读取本地 GDP
-> 输出结果、writeback_plan、报告和记忆候选
-> 审核后继续写回本地 GDP 或 memory/YYYY-MM-DD.md
```

`data/` 是本项目搭建的本地 GDP，不是外部系统镜像。飞书聊天、会议纪要和附件解析默认是候选事实；人工确认或明确审核后才能成为已确认事实。

## 本地 GDP 详细说明

本地 GDP 位于 `workspace-product-expert/data/`。`catalog.json` 是索引，定义每张表的文件路径、主键和匹配键。各表中的 `schema` 是字段说明，`records` 是真实业务数据。`records` 为空表示尚未导入真实数据，不表示表缺失；agent 可以读取 schema 判断字段要求，但不能基于空表输出正式业务结论。

### GDP 表清单

| 序号 | 逻辑表 | 文件 | 主键 | 主要用途 | 主要字段 |
| ---: | --- | --- | --- | --- | --- |
| 1 | 客户画像表 | `customer_profile.json` | `customer_id` | 记录客户行业、区域、规模、等级、联系人、决策链和历史业务摘要。 | `customer_name`、`industry`、`region`、`scale`、`level`、`contacts`、`decision_chain`、`historical_demands`、`historical_solutions`、`historical_orders`、`service_summary`、`roi_summary` |
| 2 | 客户需求主表 | `demand_master.json` | `demand_id` | 原始需求主表，承载客户需求、项目背景、年度需求、采购计划、储能识别、需求准入和需求说明书路径。 | `customer_name`、`project_name`、`project_background`、`business_pain_points`、`construction_goals`、`application_scenario`、`annual_demand_total`、`procurement_plan`、`is_storage_project`、`roi_data_completeness`、`demand_completeness_score`、`allow_solution_generation`、`missing_information`、`demand_brief_path` |
| 3 | 方案主表 | `solution_master.json` | `solution_id` | 记录方案版本、模板、配置、ROI 关联、方案状态、客户赋能、客户承认、订单转化、风险和交付边界。 | `demand_id`、`product_line`、`business_line`、`solution_type`、`word_template_id`、`contains_roi`、`roi_id`、`solution_status`、`customer_enablement_status`、`customer_ack_status`、`converted_to_order`、`order_id`、`risk_level`、`configuration_list`、`delivery_boundary`、`acceptance_requirements` |
| 4 | 订单/商机主表 | `order_master.json` | `order_id` | 记录商机阶段、订单状态、订单金额、采购计划、报价节点、合同节点、转化状态和交付范围。 | `opportunity_id`、`solution_id`、`demand_id`、`order_status`、`order_amount`、`procurement_plan`、`quote_node`、`contract_node`、`contract_status`、`conversion_status`、`non_conversion_reason`、`delivery_scope` |
| 5 | 交付项目表 | `delivery_project.json` | `delivery_id` | 记录已承认方案转交付后的责任人、责任矩阵、交付边界、验收要求、交付 9 件套路径和运行数据回流字段。 | `solution_id`、`order_id`、`delivery_owner`、`fae_owner`、`after_sales_owner`、`customer_side_owners`、`responsibility_matrix`、`delivery_boundary`、`acceptance_requirements`、`handoff_document_paths`、`operation_data_fields`、`handoff_status` |
| 6 | 现场勘查表 | `site_survey.json` | `survey_id` | 记录交付现场条件，用于交付 9 件套、实施计划和风险检查。 | `solution_id`、`order_id`、`site`、`power`、`network`、`grid_connection`、`fire_safety`、`environment`、`access_conditions`、`site_risks` |
| 7 | 文档索引表 | `document_library.json` | `document_id` | 记录需求说明书、方案书、客户确认页、合同、验收模板、运维手册、交付 9 件套、ROI 报告和复盘报告路径。 | `document_type`、`solution_id`、`demand_id`、`order_id`、`path`、`version`、`review_status`、`owner`、`source`、`related_skill` |
| 8 | 储能 ROI 测算主表 | `roi_measurement.json` | `roi_id` | 记录户储/工商储 ROI 测算、收益口径、回收期、ROI、IRR、NPV、审核状态、偏差和校准候选。 | `solution_id`、`demand_id`、`storage_type`、`region`、`storage_power`、`storage_capacity`、`total_investment`、`annual_gross_revenue`、`annual_net_revenue`、`static_payback_period`、`dynamic_payback_period`、`roi`、`irr`、`npv`、`calculation_status`、`reviewer`、`calibration_status` |
| 9 | ROI 参数表 | `roi_parameter.json` | `parameter_id` | 记录电价、负荷、成本、补贴、默认假设和审核状态，供 ROI 测算和模型校准使用。 | `region`、`storage_type`、`tariff`、`load`、`cost`、`subsidy`、`assumptions`、`source`、`review_status` |
| 10 | 客户赋能记录表 | `enablement_records.json` | `enablement_id` | 记录客户资料包、方案一页纸、客户查看状态、反馈、异议和客户承认推进状态。 | `solution_id`、`materials`、`view_status`、`feedback_status`、`ack_status`、`feedback`、`objections`、`started_at`、`completed_at` |
| 11 | FAQ 记录表 | `faq_records.json` | `faq_id` | 记录销售、客户、FAE 和交付问答、专家修正、采纳状态和知识库候选。 | `question`、`answer`、`category`、`status`、`source`、`product_line`、`expert_correction`、`adopted`、`source_evidence`、`reviewer` |
| 12 | FAE/服务记录表 | `service_records.json` | `service_id` | 记录技术支持、运维问题、故障处理、专家转接和 FAQ 候选。 | `solution_id`、`order_id`、`issue_type`、`question`、`resolution`、`expert_escalation`、`faq_candidate`、`service_status`、`service_owner`、`occurred_at`、`closed_at` |
| 13 | 储能运行数据表 | `operation_data.json` | `operation_id` | 记录储能项目实际运行数据，用于 ROI 偏差分析和模型校准。 | `solution_id`、`order_id`、`roi_id`、`storage_type`、`window_start`、`window_end`、`charge_kwh`、`discharge_kwh`、`cycles`、`availability`、`degradation`、`actual_revenue`、`tariff_snapshot`、`load_snapshot`、`operation_strategy`、`ems_parameters` |
| 14 | Word 模板使用记录表 | `template_usage.json` | `usage_id` | 记录方案生成时使用的 Word 模板版本、复用状态和退回原因。 | `solution_id`、`template_id`、`version`、`reuse_status`、`return_reason`、`created_at`、`source` |
| 15 | 标准包使用记录表 | `standard_package_usage.json` | `usage_id` | 记录标准包匹配结果、匹配理由、复用状态和审核状态。 | `solution_id`、`package_name`、`scenario`、`match_reason`、`reuse_status`、`review_status`、`created_at`、`source` |
| 16 | 数据同步运行记录 | `sync_runs.json` | `run_id` | 记录每次 `data-sync-skill` 运行状态、处理文件、表级写入数量和错误。 | `started_at`、`finished_at`、`status`、`source`、`files`、`tables`、`error_count`、`errors` |

### GDP 数据进入方式

真实数据进入本地 GDP 前，必须先进入 `data/inbox/*.json`：

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

进入路径：

1. `inbox-normalize-skill` 从客户导入、飞书聊天、会议纪要、附件文本、服务记录或运行数据中抽取结构化记录。
2. 新记录按 `references/id-rules.md` 生成主键。
3. 归一化文件写入 `data/inbox/*.json`。
4. `data-sync-skill` 按 `catalog.json` 将记录 upsert 到对应 `data/*.json` 表。
5. 同步运行结果写入 `sync_runs.json`。

### 主键和去重规则

`data-sync-skill` 不为缺少主键的记录自动造号。新记录必须在进入 `data/inbox/*.json` 前生成主键。

常用编号格式：

| 表 | 主键格式 |
| --- | --- |
| `customer_profile` | `CUST-YYYYMMDD-NNN` |
| `demand_master` | `D-YYYYMMDD-NNN` |
| `solution_master` | `S-YYYYMMDD-NNN` |
| `order_master` | `O-YYYYMMDD-NNN` |
| `roi_measurement` | `ROI-YYYYMMDD-NNN` |
| `faq_records` | `FAQ-YYYYMMDD-NNN` |
| `service_records` | `SRV-YYYYMMDD-NNN` |
| `operation_data` | `OP-YYYYMMDD-NNN` |

去重优先级：

1. 已有主键完全匹配。
2. 客户名称 + 项目名称 + 业务阶段匹配。
3. 来源消息 ID、文档路径或附件 hash 匹配。
4. 文本相似但证据不足时，标记为 `待确认`，不得静默合并。

### 写回和审核规则

业务 skill 产生本地 GDP 变更时，必须输出 `writeback_plan`，说明：

- 目标表
- 主键
- 写入字段
- 来源证据
- 数据状态或审核状态
- 是否允许覆盖原字段

禁止覆盖：

- `已审核`
- `已承认`
- `可外发`
- `人工确认`
- 其他明确人工审核结论

飞书聊天、会议纪要和附件解析默认是候选事实，应写 `data_status=待确认` 或等价状态。ROI、认证、技术参数、交付周期和合同级承诺必须保留审核角色，不能由 agent 自动变成正式结论。

## Skills

| 序号 | Skill | 具体功能 | 主要读写对象 |
| ---: | --- | --- | --- |
| 1 | `inbox-normalize-skill` | 把客户导入、飞书聊天、会议纪要、附件文本、服务记录、运行数据整理成 `data/inbox/*.json` 归一化文件，并按 `id-rules.md` 生成候选主键。 | 写 `data/inbox/*.json` |
| 2 | `data-sync-skill` | 读取 `data/inbox/*.json`，按 `catalog.json` upsert 到本地 GDP，并记录同步批次、写入数量、跳过数量和错误。 | 写所有 `data/*.json`、`sync_runs.json` |
| 3 | `demand-intake-skill` | 从销售输入、飞书消息、会议纪要、客户邮件或表单中抽取客户、项目、年度需求、采购计划、风险和限制，形成标准需求记录。 | 写回计划到 `demand_master.json` |
| 4 | `customer-profile-skill` | 从本地 GDP 读取客户画像、历史需求、历史方案、历史订单、服务记录和 ROI 记录，输出客户上下文和待销售确认问题。 | 读写 `customer_profile.json` |
| 5 | `scenario-detect-skill` | 判断新建、替换、扩容、改造、集成、试点、投标、年度框架等应用场景，输出置信度、证据和澄清问题。 | 写回计划到 `demand_master.json` |
| 6 | `storage-project-detect-skill` | 判断是否为储能项目，区分户用储能和工商储，检查 ROI 前置字段完整度，并决定后续 ROI skill。 | 写回计划到 `demand_master.json` |
| 7 | `demand-gate-skill` | 按客户信息、项目需求、应用场景、年度需求、采购计划、风险限制和储能 ROI 前置数据计算需求完整度，判断是否允许进入方案。 | 写回计划到 `demand_master.json` |
| 8 | `requirement-brief-skill` | 生成《客户需求与项目说明书》，作为正式 Word 方案书生成前置材料，并登记文档路径。 | 写 `document_library.json`、`demand_master.json` |
| 9 | `home-storage-roi-skill` | 执行户用储能 ROI 初筛、标准测算和投资决策测算，输出回收期、ROI、IRR、NPV、收益分项、敏感性和审核状态。 | 写 `roi_measurement.json`、`solution_master.json` |
| 10 | `ci-storage-roi-skill` | 执行工商储 ROI 测算，计算峰谷套利、需量管理、光伏自用提升、现金流、ROI、IRR、NPV 和充放电策略。 | 写 `roi_measurement.json`、`solution_master.json` |
| 11 | `solution-word-draft-skill` | 基于需求说明书、标准 Word 模板、标准包、配置清单和 ROI 测算结果生成技术方案书初稿。 | 写 `solution_master.json`、`document_library.json`、`template_usage.json` |
| 12 | `standard-package-match-skill` | 根据应用场景、行业、项目目标、产品线和储能类型匹配 15 类标准包，输出主标准包、辅助标准包和不适用原因。 | 写 `standard_package_usage.json`、`solution_master.json` |
| 13 | `solution-risk-review-skill` | 检查技术、认证、交付、商务、ROI 和竞品风险，输出风险等级、审核角色、待确认事项和外发控制建议。 | 写 `solution_master.json`、`document_library.json` |
| 14 | `customer-enablement-skill` | 生成客户资料包、一页纸摘要、管理层材料、技术评审材料、采购确认材料、ROI 一页纸、客户 FAQ 和讲解脚本。 | 写 `enablement_records.json`、`solution_master.json`、`document_library.json` |
| 15 | `delivery-handoff-skill` | 从已承认方案或已转订单方案生成交付 9 件套、实施计划、验收标准、项目移交资料和储能运行数据采集字段。 | 写 `delivery_project.json`、`document_library.json`、`site_survey.json` |
| 16 | `fae-support-skill` | 支持技术问答、运维问答、认证问答、故障排查和专家转接，输出 FAQ 候选和服务处理记录。 | 写 `service_records.json`、`faq_records.json` |
| 17 | `faq-memory-skill` | 汇总销售、客户、FAE 和交付问答，去重归类，生成 FAQ 候选、待专家确认问题、专家修正和知识库更新候选。 | 写 `faq_records.json`、`memory/YYYY-MM-DD.md` |
| 18 | `roi-calibration-skill` | 用实际运行数据对比原始 ROI 测算，计算收益偏差率，分析偏差来源，生成模型校准和参数修正建议。 | 写 `roi_measurement.json`、`roi_parameter.json`、`document_library.json` |
| 19 | `review-report-skill` | 生成需求、方案、客户赋能、订单转化、FAQ、ROI、模板标准包、交付服务的周报、月报、季报、年报和优化建议。 | 写 `document_library.json`、`memory/YYYY-MM-DD.md` |

## 定时任务

所有 cron 当前都配置为 `sessionTarget=isolated`，通过飞书 `announce` 输出结果，且不得覆盖人工审核结论。

| 序号 | 任务名 | 频率 | Cron | 时间区 | 使用 Skill | 主要功能 |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `sync-gdp-feishu-data` | 每天 07:10 | `10 7 * * *` | Asia/Shanghai | `inbox-normalize-skill`、`data-sync-skill` | 将客户导入、飞书提取、附件解析、服务记录、ROI 和运行数据整理进 inbox，再写入本地 GDP。 |
| 2 | `scan-incomplete-demands` | 每天 08:30 | `30 8 * * *` | Asia/Shanghai | `demand-gate-skill` | 扫描未通过准入或待补充需求，输出完整度、缺失项、销售补充问题和方案工程风险。 |
| 3 | `daily-faq-collect` | 每天 18:00 | `0 18 * * *` | Asia/Shanghai | `faq-memory-skill` | 汇总当天销售、客户和 FAE 问答，输出 FAQ 候选、待专家确认问题和知识库更新候选。 |
| 4 | `weekly-demand-quality-report` | 每周一 09:00 | `0 9 * * 1` | Asia/Shanghai | `demand-gate-skill`、`review-report-skill` | 输出上周需求完整率、退回率、退回原因、缺失字段分布、销售补采建议和规则优化候选。 |
| 5 | `weekly-faq-report` | 每周一 09:20 | `20 9 * * 1` | Asia/Shanghai | `faq-memory-skill`、`review-report-skill` | 输出上周高频 FAQ、未解决问题、专家修正清单、AI 答案采纳率和知识库更新建议。 |
| 6 | `weekly-sales-conversion-report` | 每周一 09:40 | `40 9 * * 1` | Asia/Shanghai | `customer-enablement-skill`、`review-report-skill` | 复盘需求、方案、赋能、承认、订单转化漏斗，输出阻塞原因和下周推进动作。 |
| 7 | `monthly-roi-report` | 每月 1 日 10:00 | `0 10 1 * *` | Asia/Shanghai | `home-storage-roi-skill`、`ci-storage-roi-skill`、`roi-calibration-skill`、`review-report-skill` | 分析户储和工商储 ROI 覆盖率、达标率、偏差率、收益口径和审核状态。 |
| 8 | `monthly-template-standard-package-report` | 每月 1 日 10:30 | `30 10 1 * *` | Asia/Shanghai | `solution-word-draft-skill`、`standard-package-match-skill`、`review-report-skill` | 分析 Word 模板复用率、标准包复用率、退回原因和模板优化建议。 |
| 9 | `quarterly-model-calibration` | 每季度首月 1 日 10:00 | `0 10 1 1,4,7,10 *` | Asia/Shanghai | `roi-calibration-skill` | 基于实际运行数据对比测算收益，输出 ROI 偏差来源、参数修正建议和待审核事项。 |
| 10 | `quarterly-business-review` | 每季度首月 1 日 15:00 | `0 15 1 1,4,7,10 *` | Asia/Shanghai | `review-report-skill` | 复盘客户画像、应用场景、产品线、区域、销售打法、方案质量、FAQ 和交付服务，输出管理层建议。 |
| 11 | `annual-knowledge-consolidation` | 每年 1 月 5 日 10:00 | `0 10 5 1 *` | Asia/Shanghai | `review-report-skill`、`faq-memory-skill`、`solution-risk-review-skill`、`roi-calibration-skill` | 生成年度 FAQ、年度方案白皮书、年度 ROI 报告、模板与标准包优化建议。 |

## 心跳机制

心跳规则定义在 `workspace-product-expert/HEARTBEAT.md`。

心跳只做轻量主动检查，不做复杂业务报告，不覆盖人工审核结论。周期性业务报告由 `jobs.json` cron 处理。

当前心跳检查项：

1. 检查 `memory/YYYY-MM-DD.md` 中是否有已确认事实需要晋升到 `MEMORY.md`。
2. 检查 `faq_records` 或记忆候选中是否有超过 7 天仍为 `待专家确认` 的 FAQ。
3. 检查 ROI 默认假设是否被报告提出修正但仍未经过 ROI 负责人审核。

如果没有需要处理的事项，返回：

```text
HEARTBEAT_OK
```

## 关键约束

- `data/` 是本项目本地 GDP，业务事实以这里的 `records` 为准。
- `data-sync-skill` 不给缺主键记录自动造号；新记录主键由 `inbox-normalize-skill` 按 `id-rules.md` 生成。
- 飞书聊天、会议纪要和附件解析默认是候选事实，不能直接当作已确认事实。
- 所有业务 skill 产生本地 GDP 变更时，必须输出 `writeback_plan`。
- 写回必须遵守 `references/writeback-contract.md`。
- 不覆盖人工审核结论，只能新增建议、风险、候选记录和待确认项。
- 储能项目 ROI 数据不足时，不输出正式投资回报结论。
- 客户外发方案、ROI 正式结论、技术承诺、认证承诺、交付周期和合同级承诺必须保留审核角色和审核状态。
