"""Configuration management for PyCode (multi-provider)."""
import os
import json
from pathlib import Path

CONFIG_DIR        = Path.home() / ".pycode"
CONFIG_FILE       = CONFIG_DIR  / "config.json"
HISTORY_FILE      = CONFIG_DIR  / "input_history.txt"
SESSIONS_DIR      = CONFIG_DIR  / "sessions"
DAILY_DIR         = SESSIONS_DIR / "daily"       # daily/YYYY-MM-DD/session_*.json
SESSION_HIST_FILE = SESSIONS_DIR / "history.json" # master: all sessions ever

# kept for backward-compat (/resume still reads from here)
MR_SESSION_DIR = SESSIONS_DIR / "mr_sessions"

DEFAULTS = {
    "model":            "ollama/gemma4:e4b",
    "max_tokens":       40000,
    "context_window":   0,
    "permission_mode":  "auto",   # auto | accept-all | manual
    "verbose":          False,
    "thinking":         None,
    "thinking_budget":  10000,
    "custom_base_url":  "",
    "max_tool_output":  32000,
    "max_agent_depth":  3,
    "max_concurrent_agents": 3,
    "session_daily_limit":   10000,
    "session_history_limit": 100000,
    "allowed_root": None,
    "shell_policy": "allow",
    "log_level": "warn",
    "log_file": None,
    "circuit_failure_threshold": 5,
    "circuit_window_seconds": 60,
    "circuit_cooldown_seconds": 120,
    "session_token_budget": None,
    "session_cost_budget":  None,
    "daily_token_budget":   None,
    "daily_cost_budget":    None,
    "auto_fanout_enabled":                  True,
    "auto_fanout_threshold":                0.4,
    "auto_fanout_max_subagents":            5,
    "auto_fanout_chunk_overlap_tokens":     200,
    "auto_agent_dup_summary_limit":         3,
    "agent_runner_subprocess":              False,
    # ── QQ Bot bridge ──────────────────────────────────────────────────────
    # qq_appid / qq_secret from https://q.qq.com developer portal
    "qq_appid":    "",
    "qq_secret":   "",
    # ── WeChat smart-reply (off by default) ────────────────────────────────
    "wechat_smart_reply":                  False,
    "wechat_smart_reply_whitelist":        [],
    "wechat_smart_reply_groups":           False,
    "wechat_smart_reply_groups_at_only":   False,
    "wechat_smart_reply_timeout_s":        300,
    "wechat_self_nickname":                "",
    "wechat_self_uid":                     "",
}


def load_config() -> dict:
    CONFIG_DIR.mkdir(exist_ok=True)
    SESSIONS_DIR.mkdir(exist_ok=True)
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            cfg.update(json.loads(CONFIG_FILE.read_text()))
        except Exception:
            pass
    if cfg.get("api_key") and not cfg.get("anthropic_api_key"):
        cfg["anthropic_api_key"] = cfg.pop("api_key")
    if not cfg.get("anthropic_api_key"):
        cfg["anthropic_api_key"] = os.environ.get("ANTHROPIC_API_KEY", "")
    if os.environ.get("ANTHROPIC_ENDPOINT"):
        cfg["anthropic_endpoint"] = os.environ["ANTHROPIC_ENDPOINT"]
    elif not cfg.get("anthropic_endpoint"):
        cfg["anthropic_endpoint"] = "https://api.anthropic.com"
    return cfg


def save_config(cfg: dict):
    CONFIG_DIR.mkdir(exist_ok=True)
    data = {k: v for k, v in cfg.items() if not k.startswith("_")}
    if data.get("permission_mode") == "accept-all":
        data.pop("permission_mode", None)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def current_provider(cfg: dict) -> str:
    from providers import detect_provider
    return detect_provider(cfg.get("model", "claude-opus-4-6"))


def has_api_key(cfg: dict) -> bool:
    """Check whether the active provider has an API key configured."""
    from providers import get_api_key
    pname = current_provider(cfg)
    key = get_api_key(pname, cfg)
    return bool(key)


def calc_cost(model: str, in_tokens: int, out_tokens: int) -> float:
    from providers import calc_cost as _cc
    return _cc(model, in_tokens, out_tokens)
