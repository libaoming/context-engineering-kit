# 上下文审计清单 — demo-agent（已完成示例）

## 第一步 · 画 CONTEXT.md
- [x] 项目根有 `CONTEXT.md`，7 层表逐层填了
- [x] 区分了静态 / 动态上下文

## 第二步 · 审 SDK 暗默认
- [x] 每个 SDK 字段都查过 default
- [x] 已知坑核对：`setting_sources`（命中！偷加载 8.3k）/ preset 动态段（命中）
- [x] 按实跑通路判定——确认本 bot 走 claude-agent-sdk，所以 setting_sources 成立

## 第三步 · cache 分层
- [x] 静态层(system+tool)排前部
- [x] 同 session 跑两次，cache_read 命中 ~1800 token
- [x] 算过账：砍 ① + 上 cache 省 ~85%

## 第四步 · 工具 schema lifecycle
- [x] 3 个工具 < 5，用 eager
- [x] 记了 MCP 首用 +0.5-2s 成本

## 第五步 · 长会话压缩
- [x] 设了 20 轮水位线 + 旧轮摘要化
- [x] history 自管在 messages list（不是框架黑盒）

## 横切 · 可观测
- [x] 每轮打 input_tokens / cache_read 日志
- [x] 改完 options 回填了 CONTEXT.md
