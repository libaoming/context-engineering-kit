#!/usr/bin/env python3
"""ce-audit · 上下文体检（首刀）

把 context-engineering-kit 的人肉 audit-checklist 升级成「跑一次就照出暗物质」的诊断工具。
定位：设计时 / 构建时一次性体检报告，NOT 运行时常驻治理。

用法：
    python3 audit.py <项目目录>              # 人读体检报告
    python3 audit.py <项目目录> --json       # 结构化输出（CI / 金标比对用）

首刀只查一条暗物质：claude-agent-sdk 的 setting_sources 默认偷加载 ~/.claude/CLAUDE.md。
后续在 checks/ 扩展更多检查项（见 features.json M2）。
"""
import argparse
import ast
import json
import os
import re
import sys

SKIP_DIRS = {".venv", "venv", ".git", "node_modules", "__pycache__", ".mypy_cache", "dist", "build"}
USER_CLAUDE_MD = os.path.expanduser("~/.claude/CLAUDE.md")


def _iter_py(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def imports_sdk(text):
    """用 AST 精确判断是否真 import claude_agent_sdk（避开 docstring/注释里的字面误触发）。"""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # 解析失败兜底：退回保守的文本匹配（真实代码行而非纯注释）
        return bool(re.search(r"^\s*(?:from|import)\s+claude_agent_sdk", text, re.M))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(n.name.split(".")[0] == "claude_agent_sdk" for n in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == "claude_agent_sdk":
                return True
    return False


def estimate_tokens(text):
    """粗估 token 量级。中文不用 len/4（会偏低约 4 倍）——CJK 按 ~0.7、其它按 ~0.25。"""
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿")
    other = len(text) - cjk
    return round(cjk * 0.7 + other * 0.25)


def check_setting_sources(root):
    """检测 claude-agent-sdk 的 setting_sources 暗物质。"""
    check = {
        "id": "setting_sources",
        "layer": "L1/L6 系统提示·记忆",
        "title": "claude-agent-sdk setting_sources 暗物质",
        "status": "na",
        "finding": "",
        "evidence": "",
        "fix": "",
    }

    py_files = list(_iter_py(root))
    uses_sdk = False
    sets_empty = False
    sets_nonempty = False
    evidence_file = ""

    empty_re = re.compile(r"setting_sources\s*=\s*\[\s*\]")
    any_re = re.compile(r"setting_sources\s*=")

    for path in py_files:
        text = _read(path)
        if imports_sdk(text):
            uses_sdk = True
        if empty_re.search(text):
            sets_empty = True
            evidence_file = path
        elif any_re.search(text):
            sets_nonempty = True
            if not evidence_file:
                evidence_file = path

    rel = lambda p: os.path.relpath(p, root) if p else ""

    if not uses_sdk:
        check["status"] = "na"
        check["finding"] = "项目未 import claude_agent_sdk，本条暗物质不存在（按实跑通路判定）。"
        return check

    if sets_empty:
        check["status"] = "green"
        check["finding"] = "已显式 setting_sources=[]，暗物质已禁。"
        check["evidence"] = rel(evidence_file)
        return check

    if sets_nonempty:
        check["status"] = "yellow"
        check["finding"] = "setting_sources 设了非空值——确认是有意加载，而非默认漏网。"
        check["evidence"] = rel(evidence_file)
        check["fix"] = "若不需要 ~/.claude 的全局配置，改成 setting_sources=[]。"
        return check

    # uses_sdk 但全项目没出现 setting_sources → 默认 ['user','project'] 生效
    check["status"] = "red"
    dark_tokens = estimate_tokens(_read(USER_CLAUDE_MD)) if os.path.exists(USER_CLAUDE_MD) else None
    if dark_tokens:
        check["finding"] = (
            f"用了 claude_agent_sdk 但全项目未设 setting_sources → 默认 ['user','project'] 生效，"
            f"每轮偷加载 {USER_CLAUDE_MD}（粗估约 {dark_tokens} token）+ skills 进 system prompt。"
        )
    else:
        check["finding"] = (
            "用了 claude_agent_sdk 但全项目未设 setting_sources → 默认 ['user','project'] 生效，"
            "每轮偷加载 ~/.claude/CLAUDE.md + skills 进 system prompt（暗物质）。"
        )
    check["evidence"] = "（全项目 .py 未出现 setting_sources= 赋值）"
    check["fix"] = "非 Claude Code 场景在 ClaudeAgentOptions 显式设 setting_sources=[]。"
    return check


_DOT = {"red": "🔴", "yellow": "🟡", "green": "🟢", "na": "⚪"}


def audit(root):
    checks = [check_setting_sources(root)]
    summary = {"red": 0, "yellow": 0, "green": 0, "na": 0}
    for c in checks:
        summary[c["status"]] += 1
    return {
        "project": os.path.basename(os.path.abspath(root.rstrip("/"))),
        "path": os.path.abspath(root),
        "checks": checks,
        "summary": summary,
    }


def render(report):
    lines = []
    lines.append(f"上下文体检 · {report['project']}")
    lines.append(f"路径 {report['path']}")
    lines.append("─" * 48)
    for c in report["checks"]:
        lines.append(f"{_DOT[c['status']]} [{c['layer']}] {c['title']}")
        lines.append(f"   {c['finding']}")
        if c["evidence"]:
            lines.append(f"   证据：{c['evidence']}")
        if c["fix"]:
            lines.append(f"   修法：{c['fix']}")
    s = report["summary"]
    lines.append("─" * 48)
    lines.append(f"小计  🔴{s['red']}  🟡{s['yellow']}  🟢{s['green']}  ⚪{s['na']}")
    lines.append("（首刀只查 setting_sources；定位=设计时诊断，非运行时治理）")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="ce-audit · 上下文体检")
    ap.add_argument("project", help="要体检的项目目录")
    ap.add_argument("--json", action="store_true", help="输出结构化 JSON")
    args = ap.parse_args()

    if not os.path.isdir(args.project):
        print(f"[ERROR] 不是目录：{args.project}", file=sys.stderr)
        sys.exit(2)

    report = audit(args.project)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render(report))
    # 退出码：有 red 则 1，方便 CI 卡口
    sys.exit(1 if report["summary"]["red"] else 0)


if __name__ == "__main__":
    main()
