"""干净样本 — 显式 setting_sources=[]，暗物质已禁。audit 应判 🟢 green。"""
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient


def build():
    options = ClaudeAgentOptions(
        system_prompt="你是招聘客服小妙。",
        permission_mode="default",
        setting_sources=[],  # CE 决策：不偷加载 ~/.claude/CLAUDE.md
    )
    return options
