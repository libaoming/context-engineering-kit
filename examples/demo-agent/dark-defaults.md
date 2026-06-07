# 暗物质坑库 — demo-agent（已完成示例）

## 本项目实测条目（按实跑通路）

本 bot 走 `claude-agent-sdk`，所以下面三条是真存在的：

| # | 暗物质 | 实测 token | 处置状态 |
|---|---|---|---|
| ① | `setting_sources` 默认偷加载 `~/.claude/CLAUDE.md` | **8.3k / 轮** | ✅ 已设 `[]`，归零 |
| ② | preset 动态段（cwd/git/platform）破坏 cache | ~200 / 轮 + 毁 cache | ✅ 已设 `exclude_dynamic_sections=True` |
| ③ | MCP tool schema deferred 首用延迟 | +0.5-2s（首轮）| 可接受，未改 |

## 不适用本通路（演示「别照搬」）

| 坑 | 为什么不存在 |
|---|---|
| OpenAI `truncation_strategy` | 本 bot 不用 OpenAI Assistants API |
| LiveKit 框架托管 history | 没用 LiveKit，history 自管在 messages list |
| realtime 黑盒压缩 | 不是端到端语音 |

> 这张「不适用」表本身就是 CE 纪律的体现：**先确认哪些坑在你这条通路根本不存在**，审计才算真做过。
