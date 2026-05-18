# TOOLS.md - 产品专家本地工具说明

## 本地 GDP

`workspace-product-expert/data/` 就是本项目搭建的本地 GDP。agent 的业务事实、过程状态、文档索引、FAQ、ROI、交付和复盘数据都以这里的 JSON 表为准。真实数据主要通过客户主动导入、飞书聊天/表格提取、附件解析、人工确认和服务/运行数据导出进入 `data/inbox/*.json`，再由 `data-sync-skill` 写入本地 GDP。

| 逻辑数据源 | 本地 GDP 文件 | 预期内容 | 主要进入方式 |
| --- | --- | --- | --- |
| 客户画像表 | `data/customer_profile.json` | 行业、区域、规模、等级、联系人、决策链、历史需求/方案/订单/服务摘要 | 客户导入、飞书提取、人工补录 |
| 客户需求主表 | `data/demand_master.json` | 客户需求主表记录 | 飞书聊天/会议纪要提取、客户表单、人工导入 |
| 方案主表 | `data/solution_master.json` | 方案状态、客户承认状态、配置清单、交付边界、验收要求、方案附件 | skill 生成、方案工程确认、人工导入 |
| 订单/商机主表 | `data/order_master.json` | 商机阶段、订单金额、转化状态、采购计划、合同节点 | 客户导入、销售补录、表格导入 |
| 交付项目表 | `data/delivery_project.json` | 交付负责人、FAE、售后、客户侧责任人、验收记录 | 已承认方案转交付、人工补录 |
| 现场勘查表 | `data/site_survey.json` | 场地、电力、网络、并网、消防、环境、安全、入场条件 | 现场勘查记录、附件提取、人工导入 |
| 文档索引表 | `data/document_library.json` | 需求说明书、方案书、客户确认页、合同、验收模板、运维手册路径 | skill 生成、附件解析、人工上传 |
| 客户赋能记录表 | `data/enablement_records.json` | 赋能材料、查看状态、客户反馈、客户承认状态 | 飞书反馈提取、会议纪要、人工确认 |
| FAQ 记录表 | `data/faq_records.json` | 问答、专家修正、采纳状态、知识库候选 | 飞书问答、服务记录、专家修正 |
| FAE/服务记录表 | `data/service_records.json` | 问答、故障、服务处理、专家转接、FAQ 候选 | 飞书群、服务单、FAE 手工补录 |
| ROI 测算主表 | `data/roi_measurement.json` | 储能 ROI、IRR、NPV、回收期、测算等级、审核状态 | ROI skill 输出、人工审核、导入 |
| ROI 参数表 | `data/roi_parameter.json` | 电价、负荷、成本、补贴、默认假设 | 人工维护、政策/电价表导入 |
| 储能运行数据表 | `data/operation_data.json` | 充放电量、循环、可用率、衰减、实际收益、运行策略 | 客户导入、EMS/监控导出、FAE 回流 |
| 模板使用记录表 | `data/template_usage.json` | Word 模板版本、复用状态、退回原因 | 方案生成留痕、复盘补录 |
| 标准包使用记录表 | `data/standard_package_usage.json` | 标准包匹配、复用状态、审核状态 | 标准包匹配留痕、复盘补录 |
| 数据同步运行记录 | `data/sync_runs.json` | 同步批次、状态、表级插入/更新/跳过和错误数量 | OpenClaw cron 运行日志 |

本地 JSON 表的 `records` 为空时，表示尚未导入真实业务数据。agent 可以读取表结构，但不能基于空表生成正式业务结论。

写回规则见 `references/writeback-contract.md`。任何 skill 生成的业务结果都应先明确目标表、主键、来源证据和审核状态；不得覆盖人工审核结论。

## OpenClaw 定时任务导入

项目根目录的 `jobs.json` 是 cron 清单。先在 OpenClaw 环境中配置好投递目标，再根据本地 OpenClaw CLI 版本导入或重新创建定时任务。

多渠道部署时，不建议依赖默认最近会话。应显式指定 `channel` 和 `to`：

```bash
openclaw cron add --name "scan-incomplete-demands" --cron "30 8 * * *" --tz "Asia/Shanghai" --session isolated --message "..." --announce --channel feishu --to "<open_id_or_chat_id>" --exact
```

## 确定性脚本

- `skills/data-sync-skill/scripts/sync_to_local_data.py`：把 `data/inbox/*.json` 的归一化导出 upsert 到 `data/*.json`。
- `skills/demand-gate-skill/scripts/score_demand.py`：根据 JSON 计算需求完整度评分。
- `skills/home-storage-roi-skill/scripts/calculate_home_storage_roi.py`：根据 JSON 计算户用储能 ROI。
- `skills/ci-storage-roi-skill/scripts/calculate_ci_storage_roi.py`：根据 JSON 计算工商储 ROI。

当脚本结果和模型判断不一致时，以脚本结果作为数值基线；模型判断只能作为假设、风险说明或待审核意见记录。
