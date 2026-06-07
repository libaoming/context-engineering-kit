# 配合 Claude Code：包成 context-audit skill

把本 kit 的模板包成一个 Claude Code skill（如 `context-audit`），开任意 LLM 项目时自动 scaffold CONTEXT.md + 审计清单，并在改上下文相关代码后提醒回填。

## 思路

CE 的纪律是「写第一行 SDK 配置前先画上下文构成表」。skill 把这条纪律变成开项目时的自动动作——和 harness-init「文档先行」同构，只是文档换成 CONTEXT.md。

## 核心流程三步

### 第 0 步 · 探测
判断这是不是 LLM 项目（grep `anthropic` / `openai` / `langchain` / `livekit` / mcp / `messages=` / `system_prompt`）。是 → 启动；否 → 不打扰。

### 第 1 步 · scaffold 机械文件
拷模板到项目根并替换占位符：

| 模板 | 目标 | 作用 |
|---|---|---|
| `templates/CONTEXT.md` | `./CONTEXT.md` | 7 层上下文构成表 |
| `templates/audit-checklist.md` | `./audit-checklist.md` | 5 步审计清单 |
| `templates/dark-defaults.md` | `./dark-defaults.md` | SDK 暗默认坑库 |

### 第 2 步 · 自动审计填充
派只读子 agent（见 `templates/agent_ops.md`）读构造 LLM 请求的代码，把 7 层表能查到的事实填进去（file:line），查不到的标「待实测」。**对实跑通路判定暗物质，不照搬坑库。**

### 第 3 步 · 报告 + 引导
报告「已识别暗物质 N 个 / 待实测 M 项」，引导先把 P0（通常是 history token 实测 + cache 可行性）排进 backlog，再写功能代码。

## 注意
- 已有 CONTEXT.md 先读再合并，别覆盖（可能描述了实跑通路的宝贵事实）。
- 子 agent 对远程/生产**只读**，改动只在本地。
- 别替用户 commit / push。
- 别急着写功能——CE 的价值在写码前。
