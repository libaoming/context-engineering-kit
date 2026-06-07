# 上下文审计清单 — {{PROJECT}}

> 写第一行 SDK 配置前逐条勾。已勾 = 真做过并有产物，不是"看着像做了"。

## 第一步 · 画 CONTEXT.md
- [ ] 项目根有 `CONTEXT.md`，7 层表逐层填了（填不出的格标「待实测」）
- [ ] 区分了静态上下文（每轮固定）和动态上下文（每轮变）

## 第二步 · 审 SDK 暗默认
- [ ] 用到的每个 SDK 字段都查过 default + 它对 7 层的影响
- [ ] 已知坑核对（见 `dark-defaults.md`）：`setting_sources` / `truncation_strategy` / preset 动态段 / 框架托管 history
- [ ] **暗物质按实跑通路判定**——确认了哪些坑在你这条通路根本不存在

## 第三步 · cache 分层
- [ ] 静态层（L1/L2/L4/L5）排在 prompt 前部
- [ ] 同 session 跑两次，`cache_read_input_tokens` 逼近静态部分总量
- [ ] 算过：静态部分每轮重发多少 token？上 cache 能省多少？

## 第四步 · 工具 schema lifecycle
- [ ] 工具数量 < 5 高频 → eager；几十上百 → deferred
- [ ] 用 deferred 的话，记了每个工具首用的 round-trip 成本
- [ ] 低延迟场景（语音/实时）确认用 eager

## 第五步 · 长会话压缩
- [ ] 设了上下文水位线（如 50k token）+ 压缩触发条件
- [ ] 会话结束落 `*_summary.json`，下次启动注入
- [ ] 确认 history 由谁托管（框架黑盒 / 自管），必要时实测增长曲线

## 横切 · 可观测
- [ ] 每轮打 `input_tokens` / `cache_read` / `cache_creation` / 耗时日志
- [ ] 改完任何上下文相关代码 → 回填 CONTEXT.md（防腐）
