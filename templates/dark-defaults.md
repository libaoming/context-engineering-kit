# 暗物质坑库 — {{PROJECT}}

> 暗物质 = 你以为没塞、实际被默默塞进每一轮的 token。
> **按实跑通路判定**：你不走某 SDK，它的坑就不存在——别照搬本表全部，只留你这条通路真有的。

## 已知 SDK / 框架暗默认

| SDK / 框架 | 暗默认行为 | 你是否知情 | 是否需覆盖 |
|---|---|---|---|
| `claude-agent-sdk` · `setting_sources` | 默认 `['user','project']`，偷加载 `~/.claude/CLAUDE.md` + skills（动辄 10k+ token）| ☐ | 非 Claude Code 场景设 `[]` |
| `claude-agent-sdk` · preset 模式 | 含 cwd/git/platform 动态段，破坏跨 session cache | ☐ | 设 `exclude_dynamic_sections=True` |
| `claude-agent-sdk` · mcp tool schema | deferred loading，每个 mcp tool 首用 +0.5–2s | ☐ | system 提示一次性 select 多 tool |
| `openai` Assistants · truncation_strategy | 默认保留全部历史，长会话爆 context | ☐ | 主动设 truncation |
| LiveKit `AgentSession` | 框架托管 chat history，随轮数线性膨胀且代码不可见 | ☐ | 实测增长曲线，必要时自管压缩 |
| 各类 realtime（端到端 speech-to-speech）| session 级一次性 instructions，历史压缩供应商黑盒自管，不可见不可控 | ☐ | 要精细 CE 改走 pipeline |
| `langchain` 各 chain | 默认带 verbose / system 模板 | ☐ | 关掉 / 换自己的模板 |

## 本项目实测条目

> [!TODO] 把上面与本项目实跑通路相关的行抄到这里，逐条核实「是否真存在」+「token 量」+「已处置」。

| # | 暗物质 | 实测 token | 处置状态 |
|---|---|---|---|
| ① | > [!TODO] 头号（通常是框架托管 history 或 setting_sources）| 待实测 | |
| ② | > [!TODO] | | |

> 经典反例提醒：别把别项目的「`setting_sources` 17k」直接抄成头号——先确认你的生产通路真的走 claude-agent-sdk。不走 = 这条不存在。
