---
name: fae-support-skill
description: "支持技术问答、运维问答、认证合规问答、故障排查和专家转接。Use when FAE, sales, delivery, or customers ask product, protocol, parameter, compatibility, deployment, maintenance, certification, or incident questions."
---

# FAE 技术支持

## Inputs

- 问题描述、故障现象、客户现场环境。
- 设备型号、配置清单、软件/固件版本、协议、接口、拓扑。
- 日志、截图、告警、操作记录、时间线。
- 产品手册、运维手册、认证文件、历史服务单。
- 问题风险类型：技术、运维、认证、合规、兼容性、安全、合同承诺。

## Input Sources

1. 用户本次输入的问题、故障现象、日志、截图和现场环境。
2. 如提供 `solution_id` 或 `order_id`，从 `../../data/solution_master.json`、`../../data/order_master.json` 读取配置和项目背景。
3. 从 `../../data/delivery_project.json` 读取交付、FAE、售后责任人和移交状态。
4. 从 `../../data/service_records.json` 读取历史故障、服务单和处理结果。
5. 从 `../../data/faq_records.json` 读取已确认 FAQ 和待专家确认问题。
6. 从 `../../data/document_library.json` 定位产品手册、运维手册、协议和认证文件。
7. 缺少依据时输出“暂无依据，需专家确认”。

## Procedure

1. 判断问题类型：咨询、配置、部署、运维、故障、认证、兼容性或高风险承诺。
2. 优先使用有出处的产品资料、手册、认证文件、服务记录和已确认 FAQ。
3. 有依据时回答，并给出来源、适用范围和限制条件。
4. 故障类问题输出排查路径：现象确认、信息采集、可能原因、验证步骤、临时措施、升级条件。
5. 高风险或无依据问题必须转专家确认。
6. 输出 FAQ 候选，供 faq-memory-skill 归并。

## Outputs

- 技术问答结果。
- 运维问答结果。
- 故障排查路径。
- 所需补充信息。
- 专家转接记录。
- FAQ 候选。
- `writeback_plan`：目标表 `service_records` 和 `faq_records`，登记服务处理、专家转接和 FAQ 候选；无依据答案不得写成已确认 FAQ。

## Error Handling

- 无依据时必须写“暂无依据，需专家确认”。
- 涉及安全、认证、合同承诺时升级审核。
- 不得凭经验编造参数、认证或承诺。
