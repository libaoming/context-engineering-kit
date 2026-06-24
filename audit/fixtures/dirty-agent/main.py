"""脏样本 — 漏设 setting_sources，暗物质生效。audit 应判 🔴 red。"""
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient


def build():
    options = ClaudeAgentOptions(
        system_prompt="你是招聘客服小妙。",
        permission_mode="default",
        # ⚠️ 没设 setting_sources → SDK 默认 ['user','project']，
        # 每轮偷加载 ~/.claude/CLAUDE.md + skills（暗物质）
    )
    return options
