---
name: home-storage-roi-skill
description: "执行户用储能 ROI 初筛、标准测算和投资决策测算，输出回收期、ROI、IRR、NPV、敏感性和审核状态。Use for residential, villa, overseas home storage, distributed PV owner, or channel annual demand ROI work."
---

# 户储 ROI 测算

## Inputs

- 户用储能 ROI JSON 输入。
- 必填字段：项目总投资、光伏年发电量、无储自用率、加储后自用率、居民购电价、余电上网电价、年放电量、峰谷价差。
- 可选字段：系统效率、补贴、虚拟电厂收益、运维成本、折现率、寿命、年衰减率。
- 数据来源和审核状态。

## Input Sources

1. 用户本次输入的户储 ROI 参数。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取客户用电、光伏、采购计划和储能前置信息。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取户储配置、容量、功率和方案边界。
4. 从 `../../data/roi_parameter.json` 按地区和户用储能类型读取电价、补贴、效率、成本默认参数。
5. 从 `../../data/roi_measurement.json` 读取既有测算版本，避免重复覆盖。
6. 如果关键参数缺失，只输出缺失清单和初步测算范围，不输出正式投资结论。

## Procedure

1. 检查户储 ROI 必填字段。
2. 使用 `scripts/calculate_home_storage_roi.py` 计算数值基线。
3. 区分保守收益、基础收益和增值收益。
4. 计算光伏自用提升收益、峰谷套利收益、年度总收益和年度净收益。
5. 计算静态回收期、动态回收期、ROI、IRR、NPV。
6. 输出推荐、谨慎、暂不建议三类投资建议，并标注审核状态。

## Outputs

- 项目总投资。
- 年度总收益和年度净收益。
- 静态回收期和动态回收期。
- ROI、IRR、NPV。
- 收益分项和收益口径。
- 敏感性分析。
- 投资建议。
- 审核状态和外发限制。
- `writeback_plan`：目标表 `roi_measurement` 和 `solution_master`，写入户储 ROI 测算版本、收益口径、审核状态和方案 ROI 关联；未审核结果不得标记可外发。

## Error Handling

- 缺少光伏、电价、容量或成本数据时，不输出正式投资结论。
- 增值收益不得混入保守收益。
- 结果未审核时只能作为内部测算草稿。
