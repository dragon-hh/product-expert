---
name: storage-project-detect-skill
description: "判断是否为储能项目，并区分户用储能和工商储，检查 ROI 前置字段和可测算等级。Use when a demand mentions storage, PV, tariff arbitrage, load, battery, PCS, EMS, backup, or investment return."
---

# 储能项目识别

## Inputs

- 项目描述、产品线、客户类型和应用场景。
- 储能相关线索：电池、PCS、BMS、EMS、光伏、备电、峰谷套利、需量管理、虚拟电厂。
- 户储参数：家庭/别墅/渠道、光伏发电量、用电量、居民电价、上网电价、储能容量和成本。
- 工商储参数：工厂/园区/商业体、负荷曲线、分时电价、最大需量、储能功率/容量、系统成本。

## Input Sources

1. 用户本次输入的项目描述、产品线和储能线索。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取项目需求和储能前置信息。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取方案产品线、配置和储能章节。
4. 从 `../../data/roi_parameter.json` 按地区、储能类型、客户或项目读取可用电价、负荷和成本参数。
5. 如果没有储能线索或项目描述，返回 `not_storage_or_unknown`。

## Procedure

1. 判断是否为储能项目。
2. 区分户用储能、工商储或未知储能类型。
3. 检查 ROI 必填字段和可测算等级：初步测算、标准测算、投资决策测算。
4. 决定后续调用 `home-storage-roi-skill` 或 `ci-storage-roi-skill`。
5. 输出缺失参数和可补采问题。

## Outputs

- is_storage_project。
- storage_type。
- roi_data_completeness。
- roi_calculation_level。
- missing_parameters。
- next_roi_skill。
- clarification_questions。
- `writeback_plan`：目标表 `demand_master`，更新 `is_storage_project`、`storage_project_type`、`roi_data_completeness` 和缺失 ROI 参数。

## Error Handling

- 无法区分储能类型时，不进入正式 ROI 测算。
- 缺少电价、负荷、容量或成本时，只输出缺失项和补采问题。
- 使用默认参数时必须标记为 `assumption`，不得当作客户确认数据。
