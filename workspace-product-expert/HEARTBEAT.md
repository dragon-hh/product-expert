# HEARTBEAT.md - 心跳检查

心跳只用于轻量主动检查。周期性业务报告由 `jobs.json` cron 负责。

## 当前检查清单

- 检查 `memory/YYYY-MM-DD.md` 中是否有已确认事实需要晋升到 `MEMORY.md`。
- 检查 `faq_records` 或记忆候选中是否有超过 7 天仍为 `待专家确认` 的 FAQ。
- 检查 ROI 默认假设是否被报告提出修正但仍未经过 ROI 负责人审核。

如果没有需要处理的事项，返回 `HEARTBEAT_OK`。
