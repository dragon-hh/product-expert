---
name: roi-calibration-skill
description: "用实际运行数据对比测算收益，计算 ROI 偏差率，分析偏差来源并生成模型校准建议。Use after storage delivery, monthly ROI review, or quarterly model calibration."
---

# ROI 模型校准

## Inputs

- 储能项目实际运行数据：充放电量、循环次数、可用率、衰减、实际收益。
- 原始 ROI 测算报告和测算版本。
- 电价、负荷、成本、运行策略、补贴、需求响应记录。
- 交付记录、运维记录、故障记录。
- 实际运行窗口和数据采集口径。

## Input Sources

1. 如提供 `roi_id`、`solution_id` 或 `order_id`，从 `../../data/roi_measurement.json` 读取原始 ROI 测算版本。
2. 从 `../../data/operation_data.json` 读取实际充放电量、循环次数、可用率、衰减和实际收益。
3. 从 `../../data/roi_parameter.json` 读取电价、负荷、成本和模型参数。
4. 从 `../../data/delivery_project.json` 读取交付状态、运行策略和责任人。
5. 从 `../../data/service_records.json` 读取故障、停机、运维和专家处理记录。
6. 实际运行数据为空时，只输出采集清单，不做模型校准结论。

## Procedure

1. 对齐原始测算版本、项目配置和实际运行窗口。
2. 计算实际收益、测算收益和 ROI 偏差率。
3. 拆解偏差来源：电价、负荷、循环次数、衰减、运行策略、成本、可用率、故障停机。
4. 判断偏差是否来自模型假设、客户运行策略、交付质量或外部政策变化。
5. 输出模型参数修正建议和待 ROI 负责人审核事项。

## Outputs

- 实际收益复盘。
- ROI 偏差率。
- 偏差原因分析。
- 模型校准报告。
- 参数修正建议。
- 待审核假设。
- `writeback_plan`：目标表 `roi_measurement`、`roi_parameter`、`document_library`，登记 ROI 偏差、校准状态、参数修正候选和校准报告；参数更新必须经 ROI 负责人审核。

## Error Handling

- 实际运行数据不足时只输出采集清单。
- 不能自动覆盖正式 ROI 模型参数。
- 校准建议必须由 ROI 负责人审核。
