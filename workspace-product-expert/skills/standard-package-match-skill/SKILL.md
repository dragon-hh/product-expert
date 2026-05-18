---
name: standard-package-match-skill
description: "根据应用场景、行业、项目类型和储能属性匹配 15 类标准包并给出引用方式。Use before proposal drafting, customer enablement, or delivery handoff when standard package reuse is needed."
---

# 标准包匹配

## Inputs

- 应用场景识别结果。
- 客户行业、区域、项目目标、产品线。
- 储能项目类型和 ROI 测算等级。
- 方案类型：标准、技术、投标、年度框架、替换改造、试点等。

## Input Sources

1. 用户本次输入的场景识别结果。
2. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取应用场景、行业、项目目标和产品线。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取既有方案类型和产品配置。
4. 从 `../../data/roi_measurement.json` 读取储能类型和 ROI 测算等级。
5. 从 `../../data/standard_package_usage.json` 读取历史匹配记录和复用状态。
6. 固定标准包定义来自 `../../references/standard-packages.md`。

## Procedure

1. 使用 `../../references/standard-packages.md` 的 15 类标准包清单。
2. 根据 primary 场景选择主标准包。
3. 根据行业、产品线、储能属性和商务场景选择辅助标准包。
4. 输出不适用标准包及排除原因。
5. 给出匹配理由、必要输入、缺失字段和方案章节引用建议。
6. 场景为 unknown 时停止匹配。

## Outputs

- 主标准包。
- 辅助标准包。
- 不适用标准包和原因。
- 匹配理由。
- 缺失字段。
- 模块引用建议。
- `writeback_plan`：目标表 `standard_package_usage` 和 `solution_master`，登记标准包匹配、复用状态和审核状态；应用场景不清楚时只写候选。

## Error Handling

- 没有应用场景时不匹配。
- 标准包证据不足时返回 `needs_solution_review`。
- 不得把标准包匹配结果当作最终工程配置。
