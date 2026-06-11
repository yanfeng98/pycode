English | [中文](docs/i18n/README.CN.MD)

<br> 

<div align="center">
  <a href="[https://github.com/SafeRL-Lab/Robust-Gymnasium](https://github.com/yanfeng98/pycode)">
    <img src="docs/media/logos/logo-5.png" alt="Logo" width="280"> 
  </a>

  
<h2 align="center" style="font-size: 30px;"><strong><em>PyCode</em></strong>: A Fast and Easy-to-Use Agent Harness Infrastructure for Long-Horizon, Multi-Model, and Tool-Using AI Systems</h2>
</div>


### Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/yanfeng98/pycode/main/scripts/install.sh | bash
```

After installation:

```bash
source ~/.zshrc     # macOS
# or: source ~/.bashrc   # Linux
pycode        # start chatting!
```

Other install methods: [pip install](#alternative-install-with-pip) | [uv install](#alternative-install-with-uv) | [run from source](#alternative-run-directly-from-source-no-install) | [full details](#installation)

---

## Content
- [Content](#content)
- [Installation](#installation)
  - [Alternative: install with `pip`](#alternative-install-with-pip)
    - [Optional extras](#optional-extras)
  - [Alternative: install with `uv`](#alternative-install-with-uv)
  - [Alternative: run directly from source (no install)](#alternative-run-directly-from-source-no-install)
- [Model Name Format](#model-name-format)
- [Trading Agent](#trading-agent)
- [Web UI](#web-ui)
- [Documentation](#documentation)
- [Quick Reference](#quick-reference)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Citation](#citation)
- [Thanks to all contributors:](#thanks-to-all-contributors)

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yanfeng98/pycode/main/scripts/install.sh | bash
```

### Alternative: install with `pip`

```bash
git clone https://github.com/yanfeng98/pycode.git
cd pycode
pip install .                       # then: pycode
git pull && pip install --force-reinstall .   # to update
```

#### Optional extras

```bash
pip install ".[voice]"      # voice input (sounddevice + faster-whisper)
pip install ".[vision]"     # clipboard image capture (Pillow)
pip install ".[autosuggest]"# typing-time slash autosuggest (prompt_toolkit)
pip install ".[browser]"    # headless browser (playwright); then: playwright install chromium
pip install ".[files]"      # PDF + Excel reading (pymupdf, openpyxl)
pip install ".[ocr]"        # image OCR (pytesseract)
pip install ".[trading]"    # trading agent (yfinance, rank-bm25)
pip install ".[qq]"         # QQ bot bridge (qq-botpy)
pip install ".[litellm]"    # AWS Bedrock / Azure / Vertex auth via litellm
pip install ".[all]"        # everything above
```

### Alternative: install with `uv`

```bash
git clone https://github.com/yanfeng98/pycode.git && cd pycode
uv tool install ".[all]"            # minimal: uv tool install .
uv tool install ".[all]" --reinstall   # update   ·   uv tool uninstall pycode
```

### Alternative: run directly from source (no install)

```bash
git clone https://github.com/yanfeng98/pycode.git && cd pycode
pip install -r requirements.txt
python pycode.py              # changes take effect immediately
```

---

## Model Name Format

Three equivalent forms are accepted:

```bash
pycode --model gpt-4o                  # 1. auto-detect by prefix
pycode --model ollama/qwen2.5-coder    # 2. provider/model
pycode --model kimi:moonshot-v1-32k    # 3. provider:model
```

**Auto-detection by prefix:** `claude-`→anthropic · `gpt-`/`o1`/`o3`→openai · `gemini-`→gemini · `moonshot-`/`kimi-`→kimi · `qwen`/`qwq-`→qwen · `glm-`→zhipu · `deepseek-`→deepseek · `MiniMax-`/`abab`→minimax · `llama`/`mistral`/`phi`/`gemma`/`mixtral`/`codellama`→ollama.

---

## Trading Agent

A built-in AI trading analysis + backtesting module (`pip install "cheetahclaws[trading]"`).

```bash
/trading analyze NVDA            # 5-phase pipeline: data → Bull/Bear debate → Judge → Risk panel → PM decision
/trading backtest AAPL dual_ma   # backtest a strategy (or let AI pick); Sharpe/Sortino/Calmar/drawdown/win-rate
```

4 strategies (`dual_ma`, `rsi_mean_reversion`, `bollinger_breakout`, `macd_crossover`), BM25 memory of past situations, US/HK/A-share + crypto markets with no-API-key data fallbacks. Guided sub-menu via `/ssj` → **Trading**.

> **Full guide:** [docs/guides/trading.md](docs/guides/trading.md)

---

## Web UI

A production-ready browser interface — real user accounts (bcrypt + JWT), SQLite-backed history, ops endpoints — served by Python stdlib + ten vanilla-JS modules (no Node.js / React / build step).

```bash
pip install 'cheetahclaws[web]'
pycode --web                  # auto-picks a free port (tries 8080)
pycode --web --port 9000 --host 0.0.0.0   # bind explicitly / open to LAN
pycode --web --no-auth        # skip login (localhost dev only)
```

Open `http://localhost:<port>/chat` — first account becomes admin. Includes streaming chat (WS) + SSE slash commands, persistent sessions with folders/search/Markdown export, tool cards, inline permission approval, settings panel, light/dark/system theme, and `/health` + `/metrics` endpoints. A full xterm.js PTY terminal lives at `/` (100% CLI parity).

> **Full guide:** [docs/guides/web-ui.md](docs/guides/web-ui.md) · **Docker / home server:** [docs/guides/docker.md](docs/guides/docker.md)

---

## Documentation

Detailed guides live in [`docs/guides/`](docs/guides/) to keep this README focused:

| Guide | What's inside |
|---|---|
| [**Features (full)**](docs/guides/features.md) | The complete feature table — every row with full detail (context compression, auto-fanout, themes, Trading/Research/Agents writeups) |
| [**Usage (all providers)**](docs/guides/usage.md) | Per-provider setup + example commands: Anthropic/OpenAI/Gemini/Kimi/Qwen/Zhipu/DeepSeek/MiniMax/litellm, and local Ollama/LM Studio/vLLM |
| [**Web UI**](docs/guides/web-ui.md) | Chat UI, PTY terminal, API endpoints, settings, auth, SSE streaming |
| [**Docker / Home Server**](docs/guides/docker.md) | Dockerfile + compose: web UI + bridges in one container, host Ollama, workspace mount |
| [**Reference**](docs/guides/reference.md) | CLI, 50+ commands, 33 built-in tools, session search, error classification, tool cache |
| [**Extensions**](docs/guides/extensions.md) | Memory, Skills, Sub-Agents, MCP servers, Plugins, Monitor, Autonomous Agents |
| [**Bridges**](docs/guides/bridges.md) | Telegram, WeChat, Slack, QQ setup + remote control from your phone |
| [**Security & env vars**](docs/guides/security.md) | Threat model, `PYCODE_*` vars, bot-token handling, Bash denylist, fs sandbox, CSRF |
| [**Voice & Video**](docs/guides/voice-and-video.md) | Offline Whisper voice input, Video factory, TTS factory |
| [**Trading**](docs/guides/trading.md) | Multi-agent analysis, backtesting, BM25 memory, data fallbacks, SSJ integration |
| [**Advanced**](docs/guides/advanced.md) | Brainstorm, SSJ, Tmux, proactive monitoring, checkpoints, plan mode, sessions, cloud sync |
| [**Comparison**](docs/guides/comparison.md) | Full positioning vs Claude Code and OpenClaw — at-a-glance tables, both sides' wins, key design differences |
| [**Recipes**](docs/guides/recipes.md) | 12 step-by-step examples: code review, remote control, research, bug fix, browse, email, PDF/Excel |
| [**FAQ**](docs/guides/faq.md) | The full FAQ (MCP, models/providers, CLI/scripting, voice) |
| [**Plugin Authoring**](docs/guides/plugin-authoring.md) · [Example](examples/example-plugin/) | Build a plugin: tools, commands, skills, MCP; starter template |
| [**Research Lab**](docs/guides/research-lab.md) | `/lab start <topic>` — autonomous multi-agent paper writing with sandboxed experiments |
| [**Agent OS**](docs/agent-os.md) · [RFC index](docs/RFC/) | The `cc_kernel/` layer + all design notes (RFC 0001-0032) |
| [**Contributing**](CONTRIBUTING.md) | Project structure, architecture guide, PR checklist |

---

## Quick Reference

```
pycode [OPTIONS] [PROMPT]

  -p, --print          Non-interactive: run prompt and exit
  -m, --model MODEL    Override model (e.g. gpt-4o, ollama/llama3.3)
  --accept-all         Auto-approve all operations (no permission prompts)
  --verbose            Show thinking blocks and per-turn token counts
  --show-tools         Show each tool call instead of a per-turn summary
                       (alias: --no-quiet; compact summary is the default)
  --thinking           Enable Extended Thinking (Claude only)
  --web                Start web server (Chat UI + PTY terminal in browser)
  --port / --host      Web server port / host (default 8080 / 127.0.0.1)
  --no-auth            Disable web password (local use only)
  --version / -h       Print version / show help
```

```bash
pycode                                          # interactive REPL, default model
pycode -m ollama/deepseek-r1:32b                # pick a model
pycode -p "Write a Python fibonacci function"   # non-interactive
pycode --accept-all -p "Init a pyproject.toml"  # CI / automation
pycode --web --port 8008 --no-auth              # browser chat + terminal
```

See the [Reference Guide](docs/guides/reference.md) for all 50+ slash commands, tools, and config options.

---

## Contributing

We welcome contributions! See the [Contributing Guide](CONTRIBUTING.md) for architecture, conventions, and the PR checklist.

```bash
git clone https://github.com/yanfeng98/pycode.git && cd pycode
pip install -r requirements.txt && pip install pytest
python -m pytest tests/ -x -q       # 341+ tests should pass
python pycode.py              # run the REPL
```

Building a plugin? See the [Plugin Authoring Guide](docs/guides/plugin-authoring.md) and the [example template](examples/example-plugin/).

---

## FAQ

A few common questions — the **full FAQ** is in [docs/guides/faq.md](docs/guides/faq.md).

**Q: How do I add an MCP server?**
```
/mcp add git uvx mcp-server-git          # or create .mcp.json in your project, then /mcp reload
```

**Q: Tool calls don't work with my local Ollama model.**
Not all models support function calling — use `qwen2.5-coder`, `llama3.3`, `mistral`, or `phi4`.

**Q: How do I connect to a remote GPU server running vLLM?**
```
/config custom_base_url=http://your-server-ip:8000/v1
/config custom_api_key=your-token
/model custom/your-model-name
```

**Q: How do I check my API cost?** Run `/cost` (shows input/output tokens + estimated USD).

**Q: Can I use multiple API keys in one session?** Yes — set all keys upfront (env or `/config`), then switch models freely; each call uses the active provider's key.

**Q: How do I set a default model across projects?** Add keys to `~/.bashrc`/`~/.zshrc` and set `{ "model": "claude-sonnet-4-6" }` in `~/.pycode/config.json`.

**Q: Can I pipe input to pycode?**
```bash
cat error.log | pycode -p "What is causing this error?"
```

**Q: How do I set up voice input?** `pip install sounddevice faster-whisper numpy`, then `/voice` in the REPL (downloads a ~150 MB Whisper model on first use). See the [full FAQ](docs/guides/faq.md) for languages + keyterm tuning.

---

## Citation
If you find the repository useful, please cite the study
``` Bash
@article{gu2026model,
  title={From Model Scaling to System Scaling: Scaling the Harness in Agentic AI},
  author={Gu, Shangding},
  journal={arXiv preprint arXiv:2605.26112},
  year={2026}
}

@article{pycode2026,
  title={PyCode: Agent Harness Infrastructure for Long-Horizon, Multi-Model, and Tool-Using AI Systems},
  author={PyCode Team},
  journal={github},
  year={2026}
}
```


---


## Thanks to all contributors:

<!-- contributors:start -->

<a href="https://github.com/chauncygu"><img src="https://avatars.githubusercontent.com/u/27274029?v=4&s=48" width="48" height="48" alt="chauncygu"/></a>
<a href="https://github.com/KevRojo"><img src="https://avatars.githubusercontent.com/u/9065636?v=4&s=48" width="48" height="48" alt="KevRojo"/></a>
<a href="https://github.com/mxh1999"><img src="https://avatars.githubusercontent.com/u/30319236?v=4&s=48" width="48" height="48" alt="mxh1999"/></a>
<a href="https://github.com/seetvn"><img src="https://avatars.githubusercontent.com/u/100040536?v=4&s=48" width="48" height="48" alt="seetvn"/></a>
<a href="https://github.com/bmaltais"><img src="https://avatars.githubusercontent.com/u/7474674?v=4&s=48" width="48" height="48" alt="bmaltais"/></a>
<a href="https://github.com/RheagalFire"><img src="https://avatars.githubusercontent.com/u/60213893?v=4&s=48" width="48" height="48" alt="RheagalFire"/></a>
<a href="https://github.com/yamaceay"><img src="https://avatars.githubusercontent.com/u/46201716?v=4&s=48" width="48" height="48" alt="yamaceay"/></a>
<a href="https://github.com/tsint"><img src="https://avatars.githubusercontent.com/u/63944253?v=4&s=48" width="48" height="48" alt="tsint"/></a>
<a href="https://github.com/albertcheng"><img src="https://avatars.githubusercontent.com/u/2686135?v=4&s=48" width="48" height="48" alt="albertcheng"/></a>
<a href="https://github.com/LostAion"><img src="https://avatars.githubusercontent.com/u/84846068?v=4&s=48" width="48" height="48" alt="LostAion"/></a>
<a href="https://github.com/lucaszhu-hue"><img src="https://avatars.githubusercontent.com/u/278269343?v=4&s=48" width="48" height="48" alt="lucaszhu-hue"/></a>
<a href="https://github.com/skint007"><img src="https://avatars.githubusercontent.com/u/37035851?v=4&s=48" width="48" height="48" alt="skint007"/></a>
<a href="https://github.com/thekbbohara"><img src="https://avatars.githubusercontent.com/u/133592644?v=4&s=48" width="48" height="48" alt="thekbbohara"/></a>

<!-- contributors:end -->
