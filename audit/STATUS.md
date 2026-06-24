# ce-audit · STATUS

把 kit 的人肉 audit-checklist 升级成可执行「上下文体检」。**定位=设计时/构建时一次性诊断报告，NOT 运行时常驻治理**（那是 Sipcode/Conduit 的红海，不碰）。

## 当前进度（2026-06-24）

- ✅ **M1 首刀完成**：setting_sources 暗物质检测，正反 fixture 金标回归 + 真实 playground 验收全绿。
  - `audit.py <项目>` → 人读体检报告；`--json` → 结构化；有 red 退出码 1（CI 卡口）。
  - 检测：用 AST 解析 import（避 docstring 假阳性）→ 再正则查 setting_sources 赋值 → red/green/yellow/na。
  - red 时读 `~/.claude/CLAUDE.md` 实际体积粗估暗物质 token（中文不用 len/4）。
  - 验收：`python3 audit/verify.py`（dirty=red / clean=green / no-sdk=na / playground=green，全 PASS）。

## 已知局限（诚实记账）

- setting_sources **赋值**检测仍走正则——注释里写 `setting_sources=[]` 会假判 green（import 已用 AST 修，赋值未）。M2 可升 AST 找 ClaudeAgentOptions keyword。
- 只查 1 条暗物质。preset 动态段 / mcp deferred / 框架托管 history 等仍未覆盖（见 features.json M2）。
- 纯静态审计，不跑真机；运行时 token 实测要接 U7 的 metrics_logger（M2.2）。

## 下一刀（M2 候选，三选一）

1. 扩检查项：preset `exclude_dynamic_sections` / mcp tool 数量阈值 / LiveKit 托管 history。
2. setting_sources 赋值检测升 AST，消灭注释假阳性。
3. 接 U7 metrics_logger 跑一轮真机采数，补「运行时体检」分支，凑齐 7 层 token 实测。

## 文件

- `audit.py` — 主入口（纯标准库，开箱即用）
- `verify.py` — 金标回归 + 真实世界验收
- `features.json` — 切片清单（M1 passing / M2 todo）
- `fixtures/{dirty,clean,no-sdk}-agent/` — 正反样本；`fixtures/expected/cases.json` — 金标
- `checks/` — 预留扩展目录（M2 检查项落这）
