"""monitor/store.py — Persistent subscription storage.

F-3 swapped JSON-file storage for the SQLite ``monitor_subscriptions``
table (in the shared ``~/.pycode/sessions.db``).  Reports get a
companion ``monitor_reports`` row.  REPL and daemon both read/write the
same tables — there is no in-memory cache, so a subscription added in
REPL is visible to the daemon scheduler on its next poll.

Public API (unchanged from the legacy JSON store): ``list_subscriptions``,
``get_subscription``, ``add_subscription``, ``remove_subscription``,
``update_last_run``.  New: ``save_report`` and ``list_reports``.

Migration: ``~/.pycode/monitor_subscriptions.json`` is imported
once on first access (tracked via ``schema_meta.monitor_migrated_from_json``);
the JSON file is kept readable for one release as fallback.
"""
from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

def _conn():
    from cc_daemon.schema import get_conn
    return get_conn()


# ── Helpers ────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_to_sub(row) -> dict:
    """Convert a sqlite3.Row to the historical dict shape callers expect."""
    recipients = []
    if row["recipients_json"]:
        try:
            recipients = json.loads(row["recipients_json"])
        except (TypeError, ValueError):
            recipients = []
    cfg: dict = {}
    if row["config_json"]:
        try:
            cfg = json.loads(row["config_json"])
        except (TypeError, ValueError):
            cfg = {}
    return {
        "id":          cfg.get("id", ""),  # legacy cosmetic id (if any)
        "topic":       row["topic"],
        "schedule":    row["schedule"],
        "channels":    recipients,
        "enabled":     bool(row["enabled"]),
        "created_at":  cfg.get("created_at", ""),
        "last_run":    row["last_run_at"],
        "next_run":    row["next_run_at"],
        "last_report": cfg.get("last_report_preview", ""),
    }


def _persist(sub: dict, *, conn=None) -> None:
    """INSERT/UPDATE a subscription row from a legacy- or new-shape dict."""
    c = conn if conn is not None else _conn()
    topic = sub["topic"]
    schedule = sub.get("schedule") or "6h"
    channels = sub.get("channels") or []
    enabled = 1 if sub.get("enabled", True) else 0
    last_run = sub.get("last_run")
    next_run = sub.get("next_run")
    cfg = {
        # Stash legacy/cosmetic fields the new schema doesn't carry as columns.
        # Keeps `_row_to_sub` round-tripping the historical dict shape.
        "id":                    sub.get("id", ""),
        "created_at":            sub.get("created_at", ""),
        "last_report_preview":   sub.get("last_report", "") or "",
    }
    c.execute(
        "INSERT INTO monitor_subscriptions "
        "  (topic, schedule, enabled, last_run_at, next_run_at, "
        "   recipients_json, config_json) "
        "VALUES (?,?,?,?,?,?,?) "
        "ON CONFLICT(topic) DO UPDATE SET "
        "  schedule=excluded.schedule, "
        "  enabled=excluded.enabled, "
        "  last_run_at=COALESCE(excluded.last_run_at, monitor_subscriptions.last_run_at), "
        "  next_run_at=COALESCE(excluded.next_run_at, monitor_subscriptions.next_run_at), "
        "  recipients_json=excluded.recipients_json, "
        "  config_json=excluded.config_json",
        (topic, schedule, enabled, last_run, next_run,
         json.dumps(channels, ensure_ascii=False),
         json.dumps(cfg, ensure_ascii=False)),
    )
    if conn is None:
        c.commit()


# ── Public API ────────────────────────────────────────────────────────────

def list_subscriptions() -> list[dict]:
    rows = _conn().execute(
        "SELECT * FROM monitor_subscriptions ORDER BY topic"
    ).fetchall()
    return [_row_to_sub(r) for r in rows]


def get_subscription(topic: str) -> Optional[dict]:
    row = _conn().execute(
        "SELECT * FROM monitor_subscriptions WHERE topic=?", (topic,)
    ).fetchone()
    return _row_to_sub(row) if row is not None else None


def add_subscription(topic: str, schedule: str = "daily",
                     channels: Optional[list[str]] = None) -> dict:
    """Add or update a subscription.  Returns the full subscription dict."""
    existing = get_subscription(topic)
    if existing is None:
        sub = {
            "id":          uuid.uuid4().hex[:8],
            "topic":       topic,
            "schedule":    schedule,
            "channels":    channels or [],
            "enabled":     True,
            "created_at":  _now_iso(),
            "last_run":    None,
            "next_run":    None,
            "last_report": "",
        }
    else:
        sub = dict(existing)
        sub["schedule"] = schedule
        if channels is not None:
            sub["channels"] = channels
    _persist(sub)
    return get_subscription(topic) or sub


def remove_subscription(topic: str) -> bool:
    c = _conn()
    cur = c.execute(
        "DELETE FROM monitor_subscriptions WHERE topic=?", (topic,)
    )
    c.commit()
    return cur.rowcount > 0


def update_last_run(topic: str, report: str) -> None:
    c = _conn()
    # Stash a 500-char preview of the latest report on the row itself
    # (mirrors the legacy behaviour); full body lives in monitor_reports.
    row = c.execute(
        "SELECT config_json FROM monitor_subscriptions WHERE topic=?",
        (topic,),
    ).fetchone()
    cfg: dict[str, Any] = {}
    if row and row["config_json"]:
        try:
            cfg = json.loads(row["config_json"])
        except (TypeError, ValueError):
            cfg = {}
    cfg["last_report_preview"] = (report or "")[:500]
    c.execute(
        "UPDATE monitor_subscriptions "
        "SET last_run_at=?, config_json=? WHERE topic=?",
        (_now_iso(), json.dumps(cfg, ensure_ascii=False), topic),
    )
    c.commit()


# ── Reports ────────────────────────────────────────────────────────────────

def _save_report_row(*, topic: str, body: str, sent_to: Iterable[str],
                     ts: Optional[str] = None, conn=None) -> str:
    c = conn if conn is not None else _conn()
    rid = uuid.uuid4().hex[:12]
    c.execute(
        "INSERT INTO monitor_reports (id, topic, ts, body, sent_to_json) "
        "VALUES (?, ?, ?, ?, ?)",
        (rid, topic, ts or _now_iso(), body or "",
         json.dumps(list(sent_to or []), ensure_ascii=False)),
    )
    if conn is None:
        c.commit()
    return rid


def save_report(topic: str, body: str,
                sent_to: Optional[Iterable[str]] = None) -> str:
    """Persist a generated monitor report.  Returns the new report id."""
    return _save_report_row(topic=topic, body=body, sent_to=sent_to or [])


def list_reports(topic: Optional[str] = None, *, limit: int = 20) -> list[dict]:
    """Most-recent reports, optionally filtered by topic."""
    c = _conn()
    if topic is None:
        rows = c.execute(
            "SELECT id, topic, ts, body, sent_to_json FROM monitor_reports "
            "ORDER BY ts DESC LIMIT ?", (limit,)
        ).fetchall()
    else:
        rows = c.execute(
            "SELECT id, topic, ts, body, sent_to_json FROM monitor_reports "
            "WHERE topic=? ORDER BY ts DESC LIMIT ?", (topic, limit)
        ).fetchall()
    out = []
    for r in rows:
        sent_to = []
        if r["sent_to_json"]:
            try:
                sent_to = json.loads(r["sent_to_json"])
            except (TypeError, ValueError):
                sent_to = []
        out.append({
            "id":      r["id"],
            "topic":   r["topic"],
            "ts":      r["ts"],
            "body":    r["body"] or "",
            "sent_to": sent_to,
        })
    return out
