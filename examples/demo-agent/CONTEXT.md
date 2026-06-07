# CONTEXT.md — demo-agent 上下文构成

> context-engineering-kit 示例：一个用 claude-agent-sdk 搭的客服 bot 做完 CE 的成品。演示「填完长什么样」+ 最经典的 setting_sources 暗物质。
> **审计对象**：`bot.py`（`query()` 单轮调用 + 3 个 MCP 工具）。
> **最后核对**：2026-06-07（维护人 baomingli）

---

## 0. 链路定性

```
用户消息 → bot.py query(prompt, options) → claude-agent-sdk → Claude → 回复
```
pipeline 式，每轮一次模型调用，7 层全部可见。

---

## 1. 七层逐层审计

| 层 | 内容 | 谁填 | token | 来源 |
|---|---|---|---|---|
| 1 系统提示 | 客服人设 + 退换货政策摘要 + 语气规则 | `options.system_prompt` | ~1200 | `bot.py:18-40` |
| 2 指令 | "一次只问一个问题""不确定就转人工" | 内嵌在 L1 | — | `bot.py:30-35` |
| 3 用户输入 | 当前用户消息 | `query(prompt=...)` | 变长 | `bot.py:58` |
| 4 结构化 IO | 无（直出自然语言）| — | — | — |
| 5 工具 | `lookup_order` / `check_stock` / `escalate`（MCP）| `options.mcp_servers` | ~600 | `bot.py:44-52` |
| 6 RAG/记忆 | 无向量库；**⚠️ setting_sources 偷加载 CLAUDE.md** | SDK 默认 | **见暗物质①** | — |
| 7 状态/历史 | 多轮 history 手动维护在 `messages` list | 自己代码 | 随轮数涨 | `bot.py:60-64` |

---

## 2. 暗物质清单

| # | 暗物质 | 风险 | 处置 |
|---|---|---|---|
| ① | **`setting_sources` 默认 `['user','project']`** | 偷加载 `~/.claude/CLAUDE.md`（实测 8.3k token）进每一轮，纯属无关内容 | ✅ 已设 `setting_sources=[]`（`bot.py:54`），输入 token 8.3k→0 |
| ② | **preset 动态段**（cwd/git/platform）| 破坏跨 session cache | ✅ 已设 `exclude_dynamic_sections=True` |
| ③ | MCP tool deferred 首用 +0.5-2s | 首条消息变慢 | 可接受（客服非实时）|

> 头号暗物质 ① 是按【实跑通路真存在】留下的——本 bot 确实走 claude-agent-sdk，所以 setting_sources 这条成立（对比：若用 OpenAI 直连就不存在）。

---

## 3. 静态 vs 动态

| | 内容 | cache 状态 |
|---|---|---|
| 静态 | L1 system(~1200) + L5 tool schema(~600) | ✅ 进 prompt cache，命中后省 ~1800 token/轮 |
| 动态 | L3 用户消息 + L7 history | — |

→ 砍掉 ① 的 8.3k + 静态上 cache 后，单轮输入 token 从 ~10.7k 降到 ~稳定命中，**省 ~85%**。

---

## 4. 长会话压缩
history 自管在 `messages` list；设了 20 轮水位线，超过则把旧轮摘要化（`bot.py:66-72`）。

## 5. 已知未解决
1. [P2] tool schema 能否也部分 deferred 降首轮延迟

## 6. 维护规则
改 `bot.py` 的 `system_prompt` / `mcp_servers` / `options` 配置 → 回填本文件。
