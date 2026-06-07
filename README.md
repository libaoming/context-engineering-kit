# context-engineering-kit · Context Engineering 脚手架

> 把「模型每轮看到的所有 token」当一等公民来设计，而不是让 SDK 默认值替你决定。
> 给任何要写 LLM agent / chat / 工作流的人。

一句话定位三件套：

```
Prompt 工程   优化「一句话」      —— 这句写得好不好
Context 工程  优化「一整轮的装配」 —— 这轮塞了什么、有没有暗物质、能不能缓存、会不会爆
Harness 工程  优化「跨轮的状态」   —— 项目/对话现在到哪了
```

**这个仓库补的是中间那段**：让你在写第一行 SDK 配置之前，先把上下文构成画清楚、把暗物质照出来。它是 [harness-kit](https://github.com/libaoming/harness-kit) 的姊妹件——CONTEXT.md 正是 harness「四件套的第四件」。

---

## 为什么需要 context engineering

一个判定标准，回答不出就说明上下文没设计、只是默认值在跑：

> **你能不能当场列出，你的 agent 这一轮喂给模型的完整上下文构成？哪些是你写的、哪些是 SDK 替你塞的、各占多少 token？**

| | 没有 CE | 有 CE（画了 CONTEXT.md）|
|---|---|---|
| 上下文构成 | 散在几个 prompt 文件 + 拼装代码 + 框架隐式行为 + 某人脑子里 | 一张可查、可传、可审计的单一视图 |
| 暗物质 | SDK 偷塞的 token 永远发现不了 | 逐层照出来、按实跑通路判定 |
| 优化 | 在那段文字里调措辞（边际改善）| 治装配：cache / 压缩 / 删暗物质（常是数量级）|
| 慢/贵/爆 | 凭感觉猜 | 照暗物质清单 + 静态动态表对症下药 |

**一句话原则：先让上下文 100% 可见，再谈优化。** 在每轮重发 3k、还带着 17k 暗物质的桶里调 prompt 措辞，就是在漏水的桶里调水温。

---

## 上下文七层次

模型每轮看到的 token 可拆成这 7 层。审计时逐层问四问：**内容是什么 / 谁来填 / 多少 token / 怎么 cache + 压缩**。

| 层 | 内容 | 谁最容易在这层埋暗物质 |
|---|---|---|
| 1 系统提示 | 角色 / 行为准则 / 边界 | SDK preset、setting_sources |
| 2 指令 | 任务特定、优先级、动态追加 | 代码拼装时丢规则 |
| 3 用户输入 | 当前 turn（语音=ASR 文本）| — |
| 4 结构化 IO | JSON schema、模板、response_format | 框架默认 |
| 5 工具集成 | MCP / function calling 的 schema | deferred 首用 round-trip |
| 6 RAG 与记忆 | 向量库、CLAUDE.md、summary | setting_sources 偷加载 |
| 7 状态与历史 | 对话历史、用户画像、stage | 框架托管 history 随轮数膨胀 |

> ⚠️ 第 1、6、7 层最容易被框架默默塞。CE 第一步不是优化，是让 7 层 100% 可见。

**五原则**：

1. **整体设计**——7 层互联，不能孤立优化一层。
2. **迭代优化**——每改一次跑 baseline 看 token/耗时/cache，不凭感觉。
3. **用户中心**——别为压 token 牺牲回答质量。
4. **可扩展性**——扛得住 10× 复杂度，一开始就分层 cache。
5. **可维护性**——CONTEXT.md 是活文档，跟业务演进。

---

## 快速开始

```bash
git clone https://github.com/libaoming/context-engineering-kit.git
cd your-llm-project

# 1. 拷核心三件：上下文构成表 + 审计清单 + 暗默认坑库
cp ~/context-engineering-kit/templates/CONTEXT.md        ./CONTEXT.md
cp ~/context-engineering-kit/templates/audit-checklist.md ./
cp ~/context-engineering-kit/templates/dark-defaults.md   ./

# 2. 全局替换占位符
#    {{PROJECT}} {{DATE}} {{OWNER}} 替成你的

# 3. 逐层填 CONTEXT.md 的 7 层表——填不出某一格，就是你的设计盲区
```

填完长什么样，最快看 `examples/demo-agent/`（一个 Claude Agent SDK 客服 bot 做完 CE 的成品）。

### 占位符

| 占位符 | 含义 | 示例 |
|---|---|---|
| `{{PROJECT}}` | 项目名 | `voice-agent` |
| `{{DATE}}` | 核对日期 | `2026-06-07` |
| `{{OWNER}}` | 维护人 | `baomingli` |

---

## 目录结构

```
context-engineering-kit/
├── README.md
├── templates/
│   ├── CONTEXT.md            ← ★旗舰：7 层上下文构成表 + 暗物质 + 生命周期
│   ├── audit-checklist.md    ← 5 步审计清单（可复制进任意项目逐条勾）
│   ├── dark-defaults.md      ← 暗物质坑库：SDK 暗默认登记表
│   ├── five-principles.md    ← 5 原则速查卡
│   ├── agent_ops.md          ← 脏活隔离子 agent（读大代码/日志只回结论）
│   ├── settings.local.json   ← Claude Code Stop hook 配置
│   └── hooks/stop-progress-append.sh
├── docs/
│   ├── methodology.md        ← 7 层 + 5 原则 + 生命周期详解
│   ├── with-claude-code.md   ← 把模板包成 context-audit skill
│   └── relation-to-harness.md← CE = 四件套第四件，与 harness-kit 的分工
└── examples/
    └── demo-agent/           ← 填好的成品：CONTEXT.md + 已勾审计 + 真实坑库
```

---

## 配合 Claude Code 自动化

可以把这套模板包成一个 `context-audit` skill：开任意 LLM 项目时自动 scaffold CONTEXT.md + 审计清单，并在改 prompt/拼装代码后提醒回填。见 `docs/with-claude-code.md`。

---

## 五步审计清单（写第一行 SDK 配置前）

- [ ] **画 CONTEXT.md**——静态表 + 动态表，逐层填四问
- [ ] **审 SDK 暗默认**——用任何字段前查 default + 它对 7 层的影响（`setting_sources` / `truncation_strategy` / preset 动态段）
- [ ] **分静态/动态设 cache**——静态层排前面冲 100% 命中，同 session 跑两次看 `cache_read`
- [ ] **工具 schema lifecycle**——少量高频 eager，几十上百 deferred（首用有 round-trip 成本）
- [ ] **长会话压缩**——设水位线 + 触发条件，会话结束落 `*_summary.json`
- [ ] **暗物质按实跑通路判定**——别照搬别项目坑库（你不走某 SDK，它的坑就不存在）
- [ ] **可观测**——每轮打 `input_tokens` / `cache_read` / 耗时日志

---

## 参考

- Anthropic — *Effective Context Engineering for AI Agents*（及 harness 系列）
- 公众号「橙研所」叙述版：《大家都在喊 context engineering，但没人告诉你怎么落地》
- 姊妹仓库 [harness-kit](https://github.com/libaoming/harness-kit) — CONTEXT.md 是它「四件套的第四件」

## License

[MIT](LICENSE) © baomingli（橙研所）
