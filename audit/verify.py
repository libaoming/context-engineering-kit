#!/usr/bin/env python3
"""ce-audit 验收 · 正反 fixture 金标回归 + 真实世界验收。

跑 audit.py 扫每个 fixture，比对 fixtures/expected/cases.json 的期望颜色。
额外：若 ~/claude-sdk-playground 存在，验证它被认成 green（真实世界，M1.4）。

全过退出 0，任一不符退出 1。不依赖 jq / 第三方库。
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "audit.py")
FIXTURES = os.path.join(HERE, "fixtures")
CASES = os.path.join(FIXTURES, "expected", "cases.json")


def status_of(project_dir, check_id="setting_sources"):
    out = subprocess.run(
        [sys.executable, AUDIT, project_dir, "--json"],
        capture_output=True, text=True,
    ).stdout
    report = json.loads(out)
    for c in report["checks"]:
        if c["id"] == check_id:
            return c["status"]
    return None


def main():
    with open(CASES, encoding="utf-8") as f:
        cases = json.load(f)

    rows = []
    ok = True

    # 1) 正反 fixture 金标回归
    for name, expected in cases.items():
        if name.startswith("_"):
            continue
        got = status_of(os.path.join(FIXTURES, name))
        passed = got == expected
        ok = ok and passed
        rows.append((name, expected, got, passed))

    # 2) 真实世界验收（M1.4）：playground 应判 green
    playground = os.path.expanduser("~/claude-sdk-playground")
    if os.path.isdir(playground):
        got = status_of(playground)
        passed = got == "green"
        ok = ok and passed
        rows.append(("claude-sdk-playground(真实)", "green", got, passed))
    else:
        rows.append(("claude-sdk-playground(真实)", "green", "SKIP(目录不存在)", True))

    w = max(len(r[0]) for r in rows)
    print(f"{'case'.ljust(w)}  期望      实得      结果")
    print("─" * (w + 28))
    for name, exp, got, passed in rows:
        print(f"{name.ljust(w)}  {exp.ljust(8)}  {str(got).ljust(8)}  {'PASS' if passed else 'FAIL'}")
    print("─" * (w + 28))
    print("全部通过 ✅" if ok else "存在 FAIL ❌")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
