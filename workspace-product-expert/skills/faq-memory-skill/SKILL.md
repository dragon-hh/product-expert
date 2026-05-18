---
name: faq-memory-skill
description: "自动采集、分类、归并、升级 FAQ，输出已确认、待确认、专家修正和知识库更新候选。Use after customer questions, FAE support, sales objections, expert corrections, or daily FAQ collection cron."
---

# FAQ 记忆沉淀

## Inputs

- 销售、客户、FAE、交付或方案工程问答记录。
- 专家修正记录和采纳记录。
- 问题来源、时间、客户、产品线、项目阶段。
- 已确认 FAQ 列表、待确认 FAQ 列表、过期 FAQ 列表。

## Input Sources

1. 用户本次输入的问答、客户异议或专家修正。
2. 从 `../../data/service_records.json` 读取 FAE、运维、故障和专家转接记录。
3. 从 `../../data/enablement_records.json` 读取客户反馈、异议和承认推进问题。
4. 从 `../../data/faq_records.json` 读取既有 FAQ、待确认问题、专家修正和采纳状态。
5. 本 skill 输出按 `../../references/writeback-contract.md` 写回本地 GDP 的 `faq_records` 候选记录；专家确认后才可标记为已确认 FAQ。
6. 如果问答来源不明，不得进入已确认 FAQ。

## Procedure

1. 对问题去重并聚类相似问法。
2. 分类：产品、技术、认证、交付、ROI、商务、竞品、运维。
3. 判断状态：已确认、待专家确认、已废弃、需合并、需拆分。
4. 对专家修正记录，保留原问题、AI 原回答、专家修正、适用范围、有效期和来源。
5. 生成知识库更新候选，不直接删除历史 FAQ。

## Outputs

- FAQ 候选列表。
- 合并建议。
- 待专家确认问题。
- 专家修正记录。
- 已废弃或过期 FAQ 标记建议。
- 知识库更新候选。
- `writeback_plan`：目标表 `faq_records`，主键 `faq_id`，状态、来源证据、专家确认要求和禁止删除历史 FAQ 说明。

## Error Handling

- 来源不明的问题不能进入已确认 FAQ。
- 冲突答案必须保留冲突并升级专家确认。
- 不得删除历史 FAQ，只能标记废弃或过期。
