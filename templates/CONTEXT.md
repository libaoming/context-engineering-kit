# CONTEXT.md — {{PROJECT}} 上下文构成

> 按 Context Engineering 方法论维护（context-engineering-kit）。把模型每轮看到的所有 token 当一等公民逐层审计。
> **审计对象**：<实跑的那条通路：哪个文件构造 LLM 请求> ⚠️ 必须对齐生产实跑通路，不是设计稿。
> **最后核对**：{{DATE}}（维护人 {{OWNER}}）

---

## 0. 链路定性（决定 7 层怎么写）

> [!TODO] 一句话画出链路：输入 → 谁构造 LLM 请求 → 模型 → 输出。
> 是 pipeline（每轮一次 chat completion，7 层可见）还是端到端 realtime 黑盒（7 层塌缩，CONTEXT.md 写不动）？

---

## 1. 七层逐层审计

> 填表四问：**内容是什么 / 谁来填 / 多少 token / 怎么 cache + 压缩**。查不到的标「待实测」，不臆造。填不出某格 = 你的设计盲区。

| 层 | 内容 | 谁填 | token | 来源(file:line) |
|---|---|---|---|---|
| 1 系统提示 | > [!TODO] | | 待实测 | |
| 2 指令 | > [!TODO] 含动态追加的规则 | | | |
| 3 用户输入 | > [!TODO] | | | |
| 4 结构化 IO | > [!TODO] schema/无 | | | |
| 5 工具 | > [!TODO] eager/deferred | | | |
| 6 RAG/记忆 | > [!TODO] 注入时机 | | | |
| 7 状态/历史 | > [!TODO] 谁托管 history | | | |

---

## 2. 暗物质清单（疑似被默默塞进 / 该测未测的 token）

> 按【实跑通路】判定，别照搬别项目坑库。

| # | 暗物质 | 风险 | 处置 |
|---|---|---|---|
| ① | > [!TODO] 框架托管 history？ | token 随轮数膨胀且不可见 | P0 待实测：dump 真实 request token |
| ② | > [!TODO] SDK 暗默认？（见 dark-defaults.md） | | |

---

## 3. 静态 vs 动态（cache 设计依据）

| | 内容 | cache 状态 |
|---|---|---|
| **静态**（每轮固定）| > [!TODO] L1 system / tool schema | 有无 prompt cache？ |
| **动态**（每轮变）| > [!TODO] L3 输入 / L7 history | — |

→ **最大优化机会**：> [!TODO] 静态部分每轮重发多少 token？能否上 cache 省 80%？

---

## 4. 长会话压缩

> [!TODO] history 谁管（框架黑盒 / 自管）？设没设水位线？会话结束落 summary 没？

---

## 5. 已知未解决

> [!TODO] 列 P0/P1/P2：token 实测 / cache 可行性 / 暗物质核对 …

---

## 6. 维护规则

改以下任一处都要回头核对本文件：
- > [!TODO] system prompt 文件
- > [!TODO] 构造 LLM 请求 / 拼装上下文的代码
- > [!TODO] SDK / LLM client 配置（cache / tool / 历史策略）
