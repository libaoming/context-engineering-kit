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

源头方法论：Anthropic harness 系列 + 公众号「橙研所」叙述版。
