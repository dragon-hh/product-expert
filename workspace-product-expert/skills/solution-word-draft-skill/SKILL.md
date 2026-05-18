---
name: solution-word-draft-skill
description: "按标准 Word 主模板和模块化章节库生成项目技术方案书初稿，不允许 AI 自由改目录。Use when a qualified requirement brief needs a technical proposal draft, configuration list, boundaries, ROI chapter, or versioned Word content."
---

# Word 方案书初稿

## Inputs

- 已通过准入的《客户需求与项目说明书》。
- Word 主模板编号、模板目录、模块化章节库。
- 产品配置库、技术协议库、认证文件库。
- 标准包匹配结果。
- 储能 ROI 测算结果和审核状态。

## Input Sources

1. 如提供 `demand_id`，从 `../../data/demand_master.json` 读取需求记录。
2. 如提供需求说明书文档编号，从 `../../data/document_library.json` 读取 `document_type=需求说明书`。
3. 如提供 `solution_id`，从 `../../data/solution_master.json` 读取既有方案版本、模板编号和方案状态。
4. 从 `../../data/standard_package_usage.json` 读取标准包匹配和审核状态。
5. 储能项目从 `../../data/roi_measurement.json` 读取 ROI 测算结果和审核状态。
6. Word 主模板、模块化章节库和认证文件通过 `../../data/document_library.json` 的文档索引定位。
7. 缺少需求说明书或模板目录时返回 `blocked`。

## Procedure

1. 确认存在需求说明书和准入状态。
2. 保持 Word 主模板目录不变，只填充字段和章节内容。
3. 引用标准包匹配结果选择模块化章节。
4. 填充客户、项目、场景、年度需求、采购计划、配置方案。
5. 填充技术边界、交付边界、验收标准、运维服务。
6. 储能项目必须引用 ROI 测算章节和风险假设。
7. 输出 V1.0 初稿和待审核清单。

## Outputs

- 技术方案书 Word 初稿内容。
- 配置清单。
- 技术边界和交付边界。
- 认证文件引用。
- 客户确认页。
- 方案版本记录。
- 待审核风险清单。
- `writeback_plan`：目标表 `solution_master`、`document_library`、`template_usage`，登记方案草稿、附件路径、模板编号和版本；正式状态必须由方案工程审核确认。

## Error Handling

- 缺少需求说明书时返回 `blocked`。
- 缺少模板目录时不得自由生成目录。
- 未审核内容必须保持 `draft` 或 `needs_solution_review`。
