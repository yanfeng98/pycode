# Advanced Features

## Brainstorm

`/brainstorm` runs a structured multi-persona AI debate over your project, then synthesizes all perspectives into an actionable plan.

### How it works

1. **Context snapshot** — reads `README.md`, `CLAUDE.md`, and root file listing from the current working directory.
2. **Agent count** — you are prompted to choose how many agents (2–100, default 5). Press Enter to use the default.
3. **Dynamic persona generation** — the model generates N expert roles tailored to your topic. Software topics get architects and engineers; geopolitics gets analysts, diplomats, and economists; business gets strategists and market experts. Falls back to built-in tech personas if generation fails.
4. **Agents debate sequentially**, each building on the previous responses.
5. **Output saved** to `brainstorm_outputs/brainstorm_YYYYMMDD_HHMMSS.md` in the current directory.
6. **Synthesis** — the main agent reads the saved file and produces a prioritized Master Plan.

**Example personas by topic:**

| Topic | Example Generated Personas |
|---|---|
| Software architecture | 🏗️ Architect · 💡 Product Innovator · 🛡️ Security Engineer · 🔧 Code Quality Lead · ⚡ Performance Specialist |
| US-Iran geopolitics | 🌍 Geopolitical Analyst · ⚖️ International Law Expert · 💰 Energy Economist · 🎖️ Military Strategist · 🕊️ Conflict Mediator |
| Business strategy | 📈 Market Strategist · 💼 Operations Lead · 🔍 Competitive Intelligence · 💡 Innovation Director · 📊 Financial Analyst |

### Usage

```
[myproject] ❯ /brainstorm
  How many agents? (2-100, default 5) > 5

[myproject] ❯ /brainstorm improve plugin architecture
  How many agents? (2-100, default 5) > 3

[myproject] ❯ /brainstorm US-Iran geopolitics
  How many agents? (2-100, default 5) > 7
```

### Example output

```
[myproject] ❯ /brainstorm medical research funding
  How many agents? (2-100, default 5) > 3
Generating 3 topic-appropriate expert personas...
Starting 3-Agent Brainstorming Session on: medical research funding
Generating diverse perspectives...
🩺 Clinical Trials Director is thinking...
  └─ Perspective captured.
⚖️ Medical Ethics Committee Member is thinking...
  └─ Perspective captured.
💰 Health Economics Policy Analyst is thinking...
  └─ Perspective captured.
✓  Brainstorming complete! Results saved to brainstorm_outputs/brainstorm_20260405_224117.md

   ── Analysis from Main Agent ──
[synthesized Master Plan streams here…]
```

### Notes

- Brainstorm uses the **currently selected model** (`/model` to check). A capable model (Claude Sonnet/Opus, GPT-4o, or a large local model) gives the best results.
- With many agents (20+) the session can take several minutes depending on model speed.
- Install `faker` (`pip install faker`) for randomized persona names; falls back to built-in names otherwise.
- Output files accumulate in `brainstorm_outputs/` — already added to `.gitignore` by v3.05.5.
- Long responses keep rendering live but show only the most recent screenful (a bounded tail window) until they finish, so duplicate/stale lines are prevented automatically. If output still looks garbled in SSH (repeated lines), run `/config rich_live=false` to fully disable Rich Live streaming.

---

## SSJ Developer Mode

`/ssj` opens a persistent interactive power menu — a single entry point for the most common development workflows, so you never have to remember command names.

<div align=center>
<img src="../media/demos/ssj_demo.gif" width="850"/>
</div>

### Menu options

| # | Name | What it does |
|---|------|--------------|
| 1 | 💡 Brainstorm | Multi-persona AI debate → Master Plan → auto-generates `brainstorm_outputs/todo_list.txt` |
| 2 | 📋 Show TODO | View `brainstorm_outputs/todo_list.txt` with ✓/○ indicators and pending task numbers |
| 3 | 👷 Worker | Auto-implement pending tasks (all, or select by number) |
| 4 | 🧠 Debate | Pick a file and choose agent count — expert panel debates design round-by-round; result saved next to the file |
| 5 | ✨ Propose | Pick a file — AI proposes specific improvements with code |
| 6 | 🔎 Review | Pick a file — structured code review with 1–10 ratings per dimension |
| 7 | 📘 Readme | Pick a file — auto-generate a professional README for it |
| 8 | 💬 Commit | Analyse git diff and suggest a conventional commit message |
| 9 | 🧪 Scan | Summarise all staged/unstaged changes and suggest next steps |
| 10 | 📝 Promote | Read the latest brainstorm output → convert ideas to `todo_list.txt` tasks |
| 11 | 🎬 Video | Launch the Video Content Factory wizard (if `modular/video` is available) |
| 12 | 🎙 TTS | Launch the TTS Content Factory wizard (if `modular/voice` is available) |
| 13 | 📡 Monitor | Launch the AI Monitor wizard — add subscriptions, run now, configure push notifications |
| 14 | 🤖 Agent | Launch the Autonomous Agent wizard — Research Assistant / Auto Bug Fixer / Paper Writer / Auto Coder / Custom |
| 0 | 🚪 Exit | Return to the main REPL |

### Usage

```
[myproject] ❯ /ssj

╭─ SSJ Developer Mode ⚡ ─────────────────────────
│
│   1.  💡  Brainstorm — Multi-persona AI debate
│   2.  📋  Show TODO  — View todo_list.txt
│   3.  👷  Worker     — Auto-implement pending tasks
│   4.  🧠  Debate     — Expert debate on a file
│   5.  ✨  Propose    — AI improvement for a file
│   6.  🔎  Review     — Quick file analysis
│   7.  📘  Readme     — Auto-generate README.md
│   8.  💬  Commit     — AI-suggested commit message
│   9.  🧪  Scan       — Analyze git diff
│  10.  📝  Promote    — Idea to tasks
│  11.  🎬  Video      — Video Content Factory
│  12.  🎙  TTS        — TTS Content Factory
│  13.  📡  Monitor    — AI subscriptions & alerts
│  14.  🤖  Agent      — Autonomous task agents
│   0.  🚪  Exit SSJ Mode
│
╰──────────────────────────────────────────────

  ⚡ SSJ » 1
  Topic (Enter for general): pycode plugin system

  # → Brainstorm spins up, saves to brainstorm_outputs/, generates todo_list.txt
  # → Menu re-opens automatically after each action

  ⚡ SSJ » 2
  # → Shows numbered pending tasks from brainstorm_outputs/todo_list.txt

  ⚡ SSJ » 3
  Task # (Enter for all, or e.g. 1,4,6): 2
  # → Worker implements task #2 and marks it done
```

### Slash command passthrough

Any `/command` typed at the `⚡ SSJ »` prompt is passed through to the REPL:

```
  ⚡ SSJ » /model gpt-4o
  # → switches model, then re-opens SSJ menu

  ⚡ SSJ » /exit
  # → exits pycode immediately
```

### Worker command

<div align=center>
<img src="../media/demos/worker_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">/worker: brainstorm → 5-task queue → auto-implement each with progress bar</center>
</div>

`/worker` (also accessible as SSJ option 3) reads `brainstorm_outputs/todo_list.txt` and auto-implements each pending task:

```
[myproject] ❯ /worker
  ✓ Worker starting — 3 task(s) to implement
    1. ○ Add animated brainstorm spinner
    2. ○ Implement Telegram typing indicator
    3. ○ Write SSJ demo GIF for README

  ── Worker (1/3): Add animated brainstorm spinner ──
  [model reads code, implements the change, marks task done]

[myproject] ❯ /worker 2,3
  # Implement only tasks 2 and 3

[myproject] ❯ /worker --path docs/tasks.md
  # Use a custom todo file

[myproject] ❯ /worker --workers 2
  # Process only the first 2 pending tasks this run
```

**Smart path detection** — if you pass a brainstorm output file (`.md`) by mistake, Worker detects it and offers to redirect to the matching `todo_list.txt` in the same folder. If that file does not yet exist, it offers to generate `todo_list.txt` from the brainstorm output first (SSJ Promote), then run Worker automatically.

### Debate command

SSJ option 4 runs a structured multi-round expert debate on any file:

```
  ⚡ SSJ » 4

  Files in brainstorm_outputs/:
    1. brainstorm_20260406_143022.md
    2. pycode.py

  File to debate #: 2
  Number of debate agents (Enter for 2): 3
  ℹ Debate result will be saved to: pycode_debate_143055.md

⚔️  Assembling expert panel...
  Expert 1: 🏗️ Architecture Lead — focus: system design & modularity
  Expert 2: 🔐 Security Engineer — focus: attack surface & input validation
  Expert 3: ⚡ Performance Specialist — focus: latency & memory usage

⚔️  Round 1/5 — Expert 1 thinking...
  [Architecture Lead gives opening argument...]

💬  Round 1/5 — Expert 2 formulating...
  [Security Engineer responds...]
  ...

📜  Drafting final consensus...
  [model writes consensus + saves transcript]
✓ Debate complete. Saved to pycode_debate_143055.md
```

- Agent count is configurable (minimum 2, default 2). Rounds are set to `agents × 2 − 1` for a full open-close structure.
- An animated spinner shows the current round and expert (`⚔️ Round 2/3 — Expert 1 thinking...`), stopping the moment that expert starts outputting.
- The full debate transcript and ranked consensus are saved to `<filename>_debate_HHMMSS.md` **in the same directory as the debated file**.

---


## Tmux Integration

<div align=center>
<img src="../media/demos/tmux_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Tmux Integration: AI splits panes, sends commands, captures output across sessions</center>
</div>

PyCode gives the AI model **direct control over tmux** — create sessions, split panes, send commands, and capture output. This is auto-detected at startup: tmux tools are only registered when a compatible binary (`tmux` on Linux/macOS, `psmux` on Windows) is found in PATH. If tmux is not installed, everything else works as normal.

### Why tmux tools

The `Bash` tool has a hard timeout (~30–120 s). Long-running tasks — training runs, servers, package builds, log monitors — get killed before they finish. With tmux tools, the AI sends the command to a **visible pane** that outlives any timeout, then uses `TmuxCapture` to read the output and react.

### Tools

| Tool | What it does |
|---|---|
| `TmuxListSessions` | List all active sessions |
| `TmuxNewSession` | Create a new session (use `detached=true` for background) |
| `TmuxNewWindow` | Add a visible tab inside an existing session |
| `TmuxSplitWindow` | Split the current pane vertically or horizontally |
| `TmuxSendKeys` | Send a command/keystrokes to any pane |
| `TmuxCapture` | Read visible text output from a pane |
| `TmuxListPanes` | List panes with index, size, and active status |
| `TmuxSelectPane` | Switch focus to a specific pane |
| `TmuxKillPane` | Close a pane |
| `TmuxListWindows` | List windows in a session |
| `TmuxResizePane` | Resize a pane (up/down/left/right) |

### Quick start

**Run a training script in a visible window:**
```
[pycode] » Open a new tmux window and run python train.py so I can watch the output
```
The AI will call `TmuxNewWindow` → `TmuxSendKeys("python train.py")`. A new tab opens immediately and you watch the output live.

**Check training progress:**
```
[pycode] » Check what the training window is printing now — has the loss gone down?
```
The AI calls `TmuxListPanes` to locate the pane, then `TmuxCapture` to read the last 50 lines and summarise.

**Split screen: server on the left, tests on the right:**
```
[pycode] » Run uvicorn main:app on the left and pytest on the right, split screen
```
The AI calls `TmuxSplitWindow(direction=horizontal)`, then `TmuxSendKeys` to each pane.

**Launch vLLM in a detached background session:**
```
[pycode] » Start a background tmux session running vLLM, don't take over this terminal
```
The AI calls `TmuxNewSession(detached=true)` then sends the vLLM launch command to that session.

### Bash tool vs Tmux tools

| | Bash tool | Tmux tools |
|---|---|---|
| Best for | Quick commands (`ls`, `git`, `pip install`) | Long-running tasks, servers, builds, monitors |
| Timeout | ~30–120 s, then killed | Never — runs in its own pane |
| Output | Returned directly to AI | Read on demand via `TmuxCapture` |
| Visibility | Hidden (background) | Visible to user in a real terminal pane |

**Rule of thumb:** use the Bash tool by default. Switch to tmux only when the command would timeout or you want the user to see it running.

---

## Shell Escape

<div align=center>
<img src="../media/demos/shell_escape_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Shell Escape: ! prefix runs commands directly — git, ls, python, pipes — no AI involvement</center>
</div>

Type `!` followed by any shell command to execute it directly without the AI intercepting:

```
[pycode] » !git status
  $ git status
On branch main
...

[pycode] » !ls -la
  $ ls -la
...

[pycode] » !python --version
  $ python --version
Python 3.11.7
```

Output prints inline and control returns to the PyCode prompt immediately. Any valid shell expression works, including pipes: `!cat log.txt | tail -20`.

---

## Proactive Background Monitoring

PyCode v3.05.2 adds a **sentinel daemon** that automatically wakes the agent after a configurable period of inactivity — no user prompt required. This enables use cases like continuous log monitoring, market script polling, or scheduled code checks.

### Quick start

```
[myproject] ❯ /proactive 5m
Proactive background polling: ON  (triggering every 300s of inactivity)

[myproject] ❯ keep monitoring the build log and alert me if errors appear

╭─ Claude ● ─────────────────────────
│ Understood. I'll check the build log each time I wake up.

[Background Event Triggered]
╭─ Claude ● ─────────────────────────
│ ⚙ Bash(tail -50 build.log)
│ ✓ → Build failed: ImportError in auth.py line 42
│ **Action needed:** fix the import before the next CI run.
```

### Commands

| Command | Description |
|---|---|
| `/proactive` | Show current status (ON/OFF and interval) |
| `/proactive 5m` | Enable — trigger every 5 minutes of inactivity |
| `/proactive 30s` | Enable — trigger every 30 seconds |
| `/proactive 1h` | Enable — trigger every hour |
| `/proactive off` | Disable sentinel polling |

Duration suffix: `s` = seconds, `m` = minutes, `h` = hours. Plain integer = seconds.

### How it works

- A background daemon thread starts when the REPL launches (paused by default).
- The daemon checks elapsed time since the last user or agent interaction every second.
- When the inactivity threshold is reached, it calls the agent with a wake-up prompt.
- The `threading.Lock` used by the main agent loop ensures wake-ups never interrupt an active session — they queue and fire after the current turn completes.
- Watcher exceptions are logged via `traceback` so failures are visible and debuggable.

### Complements SleepTimer

| | `SleepTimer` | `/proactive` |
|---|---|---|
| Who initiates | The agent | The user |
| Trigger | After a fixed delay from now | After N seconds of inactivity |
| Use case | "Check back in 10 minutes" | "Keep watching until I stop typing" |

---

## Checkpoint System

<div align=center>
<img src="../media/demos/checkpoint_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Checkpoint / Rewind: AI breaks tests → /checkpoint list → rewind → files restored</center>
</div>

PyCode automatically snapshots your conversation and any edited files after every turn, so you can always rewind to an earlier state.

### How it works

- **Auto-snapshot** — after each turn, the checkpoint system saves the current conversation messages, token counts, and a copy-on-write backup of every file that was written or edited that turn.
- **100-snapshot sliding window** — older snapshots are automatically evicted when the limit is reached.
- **Throttling** — if nothing changed (no new messages, no file edits) since the last snapshot, the snapshot is skipped.
- **Initial snapshot** — captured at session start, so you can always rewind to a clean slate.
- **Storage** — `~/.pycode/checkpoints/<session_id>/` (snapshots metadata + backup files).

### Commands

| Command | Description |
|---|---|
| `/checkpoint` | List all snapshots for the current session |
| `/checkpoint <id>` | Rewind: restore files to their state at snapshot `<id>` and trim conversation to that point |
| `/checkpoint clear` | Delete all snapshots for the current session |
| `/rewind` | Alias for `/checkpoint` |

### Example

```
[myproject] ❯ /checkpoint
  Checkpoints (4 total):
  #1  [turn 0] 14:02:11  "(initial state)"           0 files
  #2  [turn 1] 14:03:45  "Create app.py"              1 file
  #3  [turn 2] 14:05:12  "Add error handling"         1 file
  #4  [turn 3] 14:06:30  "Explain the code"           1 file

[myproject] ❯ /checkpoint 2
  Rewound to checkpoint #2 (turn 1)
  Restored: app.py
  Conversation trimmed to 2 messages.
```

---

## Plan Mode

<div align=center>
<img src="../media/demos/plan_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Plan Mode: Read-only analysis → write plan → /plan done → implement</center>
</div>

Plan mode is a structured workflow for tackling complex, multi-file tasks: Claude first analyses the codebase in a read-only phase and writes an explicit plan, then the user approves before implementation begins.

### How it works

In plan mode:
- **Only reads** are permitted (`Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, safe `Bash` commands).
- **Writes are blocked** everywhere **except** the dedicated plan file (`.pycode/plans/<session_id>.md`).
- Blocked write attempts produce a helpful message rather than prompting the user.
- The system prompt is augmented with plan mode instructions.
- After compaction, the plan file context is automatically restored.

### Slash command workflow

```
[myproject] ❯ /plan add WebSocket support
  Plan mode activated.
  Plan file: .pycode/plans/a3f9c1b2.md
  Reads allowed. All other writes blocked (except plan file).

[myproject] ❯ <describe your task>
  [Claude reads files, builds understanding, writes plan to plan file]

[myproject] ❯ /plan
  # Plan: Add WebSocket support

  ## Phase 1: Create ws_handler.py
  ## Phase 2: Modify server.py to mount the handler
  ## Phase 3: Add tests

[myproject] ❯ /plan done
  Plan mode exited. Permission mode restored to: auto
  Review the plan above and start implementing when ready.

[myproject] ❯ /plan status
  Plan mode: INACTIVE  (permission mode: auto)
```

### Agent tool workflow (autonomous)

Claude can autonomously enter and exit plan mode using the `EnterPlanMode` and `ExitPlanMode` tools — both are auto-approved in all permission modes:

```
User: Refactor the authentication module

Claude: [calls EnterPlanMode(task_description="Refactor auth module")]
  → reads auth.py, users.py, tests/test_auth.py ...
  → writes plan to .pycode/plans/...
  [calls ExitPlanMode()]
  → "Here is my plan. Please review and approve before I begin."

User: Looks good, go ahead.
Claude: [implements the plan]
```

### Commands

| Command | Description |
|---|---|
| `/plan <description>` | Enter plan mode with a task description |
| `/plan` | Print the current plan file contents |
| `/plan done` | Exit plan mode, restore previous permissions |
| `/plan status` | Show whether plan mode is active |

---

## Context Compression

Long conversations are automatically compressed to stay within the model's context window.

**Two layers:**

1. **Snip** — Old tool outputs (file reads, bash results) are truncated after a few turns. Fast, no API cost.
2. **Auto-compact** — When token usage exceeds 70% of the context limit, older messages are summarized by the model into a concise recap.

This happens transparently. You don't need to do anything.

**Manual compaction** — You can also trigger compaction at any time with `/compact`. An optional focus string tells the summarizer what context to prioritize:

```
[myproject] ❯ /compact
  Compacted: ~12400 → ~3200 tokens (~9200 saved)

[myproject] ❯ /compact keep the WebSocket implementation details
  Compacted: ~11800 → ~3100 tokens (~8700 saved)
```

If plan mode is active, the plan file context is automatically restored after any compaction.

---

## Diff View

When the model edits or overwrites a file, you see a git-style diff:

```diff
  Changes applied to config.py:

--- a/config.py
+++ b/config.py
@@ -12,7 +12,7 @@
     "model": "claude-opus-4-6",
-    "max_tokens": 8192,
+    "max_tokens": 16384,
     "permission_mode": "auto",
```

Green lines = added, red lines = removed. New file creations show a summary instead.

---

## CLAUDE.md Support

Place a `CLAUDE.md` file in your project to give the model persistent context about your codebase. PyCode automatically finds and injects it into the system prompt.

```
~/.claude/CLAUDE.md          # Global — applies to all projects
/your/project/CLAUDE.md      # Project-level — found by walking up from cwd
```

**Example `CLAUDE.md`:**

```markdown
# Project: FastAPI Backend

## Stack
- Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic
- Tests: pytest, coverage target 90%

## Conventions
- Format with black, lint with ruff
- Full type annotations required
- New endpoints must have corresponding tests

## Important Notes
- Never hard-code credentials — use environment variables
- Do not modify existing Alembic migration files
- The `staging` branch deploys automatically to staging on push
```

---

## Session Management

### Storage layout

Every exit automatically saves to three places:

```
~/.pycode/sessions/
├── history.json                          ← master: all sessions ever (capped)
├── mr_sessions/
│   └── session_latest.json              ← always the most recent (/resume)
└── daily/
    ├── 2026-04-05/
    │   ├── session_110523_a3f9.json     ← per-day files, newest kept
    │   └── session_143022_b7c1.json
    └── 2026-04-04/
        └── session_183100_3b4c.json
```

Each session file includes metadata:

```json
{
  "session_id": "a3f9c1b2",
  "saved_at": "2026-04-05 11:05:23",
  "turn_count": 8,
  "messages": [...]
}
```

### Autosave on exit

Every time you exit — via `/exit`, `/quit`, `Ctrl+C`, or `Ctrl+D` — the session is saved automatically:

```
✓ Session saved → /home/.../.pycode/sessions/mr_sessions/session_latest.json
✓              → /home/.../.pycode/sessions/daily/2026-04-05/session_110523_a3f9.json  (id: a3f9c1b2)
✓   history.json: 12 sessions / 87 total turns
```

### Quick resume

To continue where you left off:

```bash
pycode
[myproject] ❯ /resume
✓  Session loaded from …/mr_sessions/session_latest.json (42 messages)
```

Resume a specific file:

```bash
/resume session_latest.json          # loads from mr_sessions/
/resume /absolute/path/to/file.json  # loads from absolute path
```

### Manual save / load

```bash
/save                          # save with auto-name (session_TIMESTAMP_ID.json)
/save debug_auth_bug           # named save to ~/.pycode/sessions/

/load                          # interactive list grouped by date
/load debug_auth_bug           # load by filename
```

**`/load` interactive list:**

```
  ── 2026-04-05 ──
  [ 1] 11:05:23  id:a3f9c1b2  turns:8   session_110523_a3f9.json
  [ 2] 09:22:01  id:7e2d4f91  turns:3   session_092201_7e2d.json

  ── 2026-04-04 ──
  [ 3] 22:18:00  id:3b4c5d6e  turns:15  session_221800_3b4c.json

  ── Complete History ──
  [ H] Load ALL history  (3 sessions / 26 total turns)  /home/.../.pycode/sessions/history.json

  Enter number(s) (e.g. 1 or 1,2,3), H for full history, or Enter to cancel >
```

- Enter a single number to load one session
- Enter comma-separated numbers (e.g. `1,3`) to merge multiple sessions in order
- Enter `H` to load the entire history — shows message count and token estimate before confirming

### Configurable limits

| Config key | Default | Description |
|---|---|---|
| `session_daily_limit` | `5` | Max session files kept per day in `daily/` |
| `session_history_limit` | `100` | Max sessions kept in `history.json` |

```bash
/config session_daily_limit=10
/config session_history_limit=200
```

### history.json — full conversation history

`history.json` accumulates every session in one place, making it possible to search your complete conversation history or analyze usage patterns:

```json
{
  "total_turns": 150,
  "sessions": [
    {"session_id": "a3f9c1b2", "saved_at": "2026-04-05 11:05:23", "turn_count": 8, "messages": [...]},
    {"session_id": "7e2d4f91", "saved_at": "2026-04-05 09:22:01", "turn_count": 3, "messages": [...]}
  ]
}
```

---

## Cloud Sync (GitHub Gist)

<div align=center>
<img src="../media/demos/cloudsave_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Cloud Sync: /cloudsave on desktop → encrypted upload → /cloudload on laptop → full session restored</center>
</div>

PyCode v3.05.3 adds optional cloud backup of conversation sessions via **GitHub Gist**. Sessions are stored as private Gists (JSON), browsable in the GitHub UI. No extra dependencies — uses Python's stdlib `urllib`.

### Setup (one-time)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Generate new token (classic)**
2. Enable the **`gist`** scope
3. Copy the token and run:

```
[myproject] ❯ /cloudsave setup ghp_xxxxxxxxxxxxxxxxxxxx
✓ GitHub token saved (logged in as: Chauncygu). Cloud sync is ready.
```

### Upload a session

```
[myproject] ❯ /cloudsave
Uploading session to GitHub Gist…
✓ Session uploaded → https://gist.github.com/abc123def456
```

Add an optional description:

```
[myproject] ❯ /cloudsave push auth refactor debug session
```

### Auto-sync on exit

```
[myproject] ❯ /cloudsave auto on
✓ Auto cloud-sync ON — session will be uploaded to Gist on /exit.
```

From that point on, every `/exit` or `/quit` automatically uploads the session before closing.

### Browse and restore

```
[myproject] ❯ /cloudsave list
  Found 3 session(s):
  abc123de…  2026-04-05 11:02  auth refactor debug session
  7f9e12ab…  2026-04-04 22:18  proactive monitoring test
  3b4c5d6e…  2026-04-04 18:31

[myproject] ❯ /cloudsave load abc123de...full-gist-id...
✓ Session loaded from Gist (42 messages).
```

### Commands reference

| Command | Description |
|---|---|
| `/cloudsave setup <token>` | Save GitHub token (needs `gist` scope) |
| `/cloudsave` | Upload current session to a new or existing Gist |
| `/cloudsave push [desc]` | Upload with optional description |
| `/cloudsave auto on\|off` | Toggle auto-upload on exit |
| `/cloudsave list` | List all pycode Gists |
| `/cloudsave load <gist_id>` | Download and restore a session |

---

## Project Structure

```
pycode/
├── pycode.py        # Entry point: REPL loop, readline setup, diff rendering, Rich Live streaming, proactive sentinel daemon, auto-start bridge wiring
├── runtime.py             # RuntimeContext singleton — live session references (run_query, handle_slash, agent_state, tg/slack/wx send + input events) shared across all modules without polluting the config dict
├── agent.py              # Agent loop: streaming, tool dispatch, compaction
├── providers.py          # Multi-provider: Anthropic, OpenAI-compat streaming
├── tools.py              # Core tools (Read/Write/Edit/Bash/Glob/Grep/Web/NotebookEdit/GetDiagnostics) + registry wiring
├── tool_registry.py      # Tool plugin registry: register, lookup, execute
├── compaction.py         # Context compression: snip + auto-summarize
├── context.py            # System prompt builder: CLAUDE.md + git + memory
├── config.py             # Config load/save/defaults; DAILY_DIR, SESSION_HIST_FILE paths
├── cloudsave.py          # GitHub Gist cloud sync (upload/download/list sessions)
│
├── ui/                   # Terminal output package
│   └── render.py         # ANSI helpers (clr/info/ok/warn/err), Rich Live Markdown renderer, spinner phrases
│
├── bridges/              # Messaging bridge package
│   ├── telegram.py       # Telegram Bot API bridge: long-poll loop, slash passthrough, input routing, typing indicator
│   ├── wechat.py         # WeChat iLink bridge: long-poll loop, context_token, typing indicator, session recovery
│   └── slack.py          # Slack Web API bridge: conversation.history poll, in-place reply update, slash passthrough
│
├── commands/             # Slash-command handlers package
│   ├── session.py        # /save /load /resume /export /copy /history
│   ├── config_cmd.py     # /config /status /doctor
│   ├── core.py           # /clear /compact /cost /verbose /thinking /image /model /init
│   ├── checkpoint_plan.py# /checkpoint /rewind /plan
│   └── advanced.py       # /brainstorm /worker /ssj /proactive /tasks /agents /skills /memory /mcp /plugin /voice /tts /video
│
├── multi_agent/          # Multi-agent package
│   ├── __init__.py       # Re-exports
│   ├── subagent.py       # AgentDefinition, SubAgentManager, worktree helpers
│   └── tools.py          # Agent, SendMessage, CheckAgentResult, ListAgentTasks, ListAgentTypes
├── subagent.py           # Backward-compat shim → multi_agent/
│
├── memory/               # Memory package
│   ├── __init__.py       # Re-exports
│   ├── types.py          # MEMORY_TYPES and format guidance
│   ├── store.py          # save/load/delete/search, MEMORY.md index rebuilding
│   ├── scan.py           # MemoryHeader, age/freshness helpers
│   ├── context.py        # get_memory_context(), truncation, AI search
│   └── tools.py          # MemorySave, MemoryDelete, MemorySearch, MemoryList
├── memory.py             # Backward-compat shim → memory/
│
├── skill/                # Skill package
│   ├── __init__.py       # Re-exports; imports builtin to register built-ins
│   ├── loader.py         # SkillDef, parse, load_skills, find_skill, substitute_arguments
│   ├── builtin.py        # Built-in skills: /commit, /review
│   ├── executor.py       # execute_skill(): inline or forked sub-agent
│   └── tools.py          # Skill, SkillList
├── skills.py             # Backward-compat shim → skill/
│
├── mcp/                  # MCP (Model Context Protocol) package
│   ├── __init__.py       # Re-exports
│   ├── types.py          # MCPServerConfig, MCPTool, MCPServerState, JSON-RPC helpers
│   ├── client.py         # StdioTransport, HttpTransport, MCPClient, MCPManager
│   ├── config.py         # Load .mcp.json (project) + ~/.pycode/mcp.json (user)
│   └── tools.py          # Auto-discover + register MCP tools into tool_registry
│
├── voice/                # Voice input package (v3.05) — backward-compat shim → modular/voice/
│   └── __init__.py       # Re-exports from modular.voice.*
│
├── video/                # Video package — backward-compat shim → modular/video/
│   └── __init__.py       # Re-exports from modular.video.*
│
├── modular/              # Plug-and-play module ecosystem (v3.05.55)
│   ├── __init__.py       # Auto-discovery registry: load_all_commands(), load_all_tools(), list_modules()
│   ├── base.py           # HasCommandDefs / HasToolDefs Protocol interface docs
│   ├── voice/            # Voice submodule (self-contained)
│   │   ├── __init__.py   # Public API: check_voice_deps, voice_input, list_input_devices
│   │   ├── cmd.py        # /voice + /tts commands; COMMAND_DEFS plug-in interface
│   │   ├── recorder.py   # Audio capture: sounddevice → arecord → sox rec
│   │   ├── stt.py        # STT: faster-whisper → openai-whisper → OpenAI API
│   │   ├── keyterms.py   # Coding-domain vocab from git branch + project files
│   │   └── tts_gen.py    # TTS pipeline: style presets, AI text gen, synthesis, run_tts_pipeline()
│   └── video/            # Video submodule (self-contained)
│       ├── __init__.py   # Re-exports
│       ├── cmd.py        # /video command; COMMAND_DEFS plug-in interface
│       ├── pipeline.py   # Full video assembly: story → TTS → images → subtitles → mp4
│       ├── story.py      # AI story generation + niche prompts
│       ├── tts.py        # TTS backends: Gemini → ElevenLabs → Edge; CJK auto-voice; chunking
│       ├── images.py     # Image backends: Gemini Web → web-search → placeholder
│       └── subtitles.py  # PIL subtitle renderer + text-to-SRT conversion
│
├── checkpoint/           # Checkpoint system (v3.05.6)
│   ├── __init__.py       # Public API exports
│   ├── types.py          # FileBackup + Snapshot dataclasses; MAX_SNAPSHOTS = 100
│   ├── store.py          # File-level backup, snapshot persistence, rewind, cleanup
│   └── hooks.py          # Write/Edit/NotebookEdit interception — backs up files before modification
│
└── tests/                # 267+ unit tests
    ├── test_mcp.py
    ├── test_memory.py
    ├── test_skills.py
    ├── test_subagent.py
    ├── test_tool_registry.py
    ├── test_compaction.py
    ├── test_diff_view.py
    ├── test_voice.py         # 29 voice tests (no hardware required)
    ├── test_checkpoint.py    # 24 checkpoint unit tests
    ├── e2e_checkpoint.py     # 10-step checkpoint lifecycle test
    ├── e2e_plan_mode.py      # 10-step plan mode permission test
    ├── e2e_plan_tools.py     # 8-step EnterPlanMode/ExitPlanMode tool test
    ├── e2e_compact.py        # 9-step compaction test
    └── e2e_commands.py       # 9-step /init /export /copy /status test
```

> **For developers:** The codebase is organized into clear layers: `runtime.py` holds live cross-module state; `ui/render.py` provides all terminal output helpers; `bridges/` contains each messaging integration; `commands/` contains REPL slash-command handlers; feature packages (`multi_agent/`, `memory/`, `skill/`, `mcp/`, `checkpoint/`) are self-contained. Add custom tools by calling `register_tool(ToolDef(...))` from any module imported by `tools.py`. To add a new plug-and-play module to the ecosystem, create `modular/<name>/cmd.py` exporting `COMMAND_DEFS = {"cmdname": {"func": callable, "help": ..., "aliases": []}}` — it is auto-discovered at startup with no registration step.

---

