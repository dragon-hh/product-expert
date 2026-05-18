---
name: ci-storage-roi-skill
description: "执行工商储 ROI 初筛、标准测算和投资决策测算，输出峰谷套利、需量管理、光伏消纳、现金流、IRR、NPV and risk assumptions. Use for factory, park, commercial complex, charging station, data center, or C&I PV storage ROI work."
---

# 工商储 ROI 测算

## Inputs

- 工商储 ROI JSON 输入。
- 必填字段：项目总投资、单日放电量、峰谷价差、年运行天数、分时电价可用状态、负荷曲线可用状态。
- 可选字段：系统效率、需量削减、需量单价、光伏多自用电量、购电价、上网电价、补贴、需求响应、虚拟电厂、运维成本、折现率、寿命、衰减率。
- 数据来源和审核状态。

## Input Sources

1. 用户本次输入的工商储 ROI 参数。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取客户行业、地区、负荷、电价和采购计划。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取储能功率、容量、配置和方案边界。
4. 从 `../../data/roi_parameter.json` 按地区和工商储类型读取分时电价、需量电费、成本、折现率等参数。
5. 从 `../../data/roi_measurement.json` 读取既有测算版本，避免重复覆盖。
6. 如果分时电价或负荷曲线缺失，不输出正式 IRR 和 NPV。

## Procedure

1. 校验分时电价、负荷曲线、最大需量、容量和成本。
2. 使用 `scripts/calculate_ci_storage_roi.py` 计算数值基线。
3. 计算峰谷套利、需量管理、光伏消纳提升和已确认补贴。
4. 单列需求响应、虚拟电厂、碳减排、扩容延缓等不确定收益。
5. 输出现金流、回收期、ROI、IRR、NPV、充放电策略和投资建议。

## Outputs

- 项目总投资。
- 收益分项。
- 年度/月度净收益。
- 静态/动态回收期。
- ROI、IRR、NPV。
- 年度现金流表。
- 充放电策略。
- 敏感性分析。
- 投资建议和审核状态。
- `writeback_plan`：目标表 `roi_measurement` 和 `solution_master`，写入工商储 ROI 测算版本、收益口径、审核状态和方案 ROI 关联；未审核结果不得标记可外发。

## Error Handling

- 没有分时电价和负荷数据，不输出正式 IRR 和 NPV。
- 不确定收益必须单列。
- 结果未审核时只能作为内部测算草稿。
