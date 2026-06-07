# CE 与 Harness 的关系

两套方法论正交、互补，常一起用。

```
Harness 工程  管「项目/任务状态」 —— 哪条 feature 真通了、新 session 怎么接班   →喂给【接班的人/agent】
Context 工程  管「上下文构成」     —— 模型这一轮看到了什么、哪里有暗物质           →喂给【模型这一整轮】
```

分水岭是**喂给谁**：Harness 的产物（STATUS.md / PROGRESS.md）给接班的人看；CE 的产物（CONTEXT.md）描述喂给模型的东西，但文档本身也是给人看的、运行时不进上下文。

## CONTEXT.md = 四件套的第四件

harness 的三件套升级为四件套：

```
features.json  +  AGENTS.md  +  PROGRESS.md  +  CONTEXT.md
└──────────── harness 三件 ────────────┘     └─ CE 产物
```

**CE 不替代 harness，是嵌进 harness 的一层。** 用 [harness-kit](https://github.com/libaoming/harness-kit) scaffold 项目时，CONTEXT.md 就是那第四件——本 kit 提供它的模板和审计方法。

## 文件分工速查

| 文件 | 属于 | 管什么 | 读者 |
|---|---|---|---|
| `STATUS.md` | harness | 项目一句话状态 + 下次入口 | 接班的人 |
| `PROGRESS.md` | harness | 里程碑内 feature 级进度 | 接班的人 |
| `features.json` | harness | 单一事实源（status） | 人 + 自动化 |
| `CONTEXT.md` | **CE** | 模型每轮上下文构成 + 暗物质 | 人（审计/优化时）|

## 什么时候各用哪个

- 新建 LLM 项目 → harness 搭骨架 + CE 同时落 CONTEXT.md（写码前）
- 改 prompt / 上下文拼装 → 先读 CONTEXT.md
- agent 半成品堆叠、接班断片 → 看 harness（STATUS/PROGRESS）
- 慢 / 贵 / 爆 context / 怪故障 → 看 CONTEXT.md（暗物质 + cache 表）

## 怎么挂进工作流（写在项目 CLAUDE.md）

CONTEXT.md 不被代码调用——运行时没有任何代码读它（它是给人/agent 看的档案，不进模型上下文）。让 agent 在对的时机读它的纪律，写在**项目级** `CLAUDE.md`，不是全局 `~/.claude/CLAUDE.md`（后者本身会被 `setting_sources` 偷塞，往里加东西是反向操作）：

```markdown
## 上下文工程纪律
改 system prompt / 上下文拼装代码前先读 CONTEXT.md，改完回填。
```

两者分工：

- `CLAUDE.md` → **自动入会**（每次 session 由 Claude Code 加载）→ 它是"调用入口"
- `CONTEXT.md` → **按需调阅**（靠 CLAUDE.md 写一句话指引才读）→ 它是"档案"
- 想更强制：加 PreToolUse **hook**，改 `system_prompt` 文件时弹出"先读 CONTEXT.md"

harness-kit 的 `CLAUDE.md` 模板已内置「上下文工程纪律（LLM 项目）」段——用它 scaffold 的项目自动把 CE 挂进工作流。

---

源头方法论：Anthropic harness 系列 + 公众号「橙研所」叙述版。
