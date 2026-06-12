"""F-3 tests for monitor/store.py — SQLite backing."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import monitor.store as store
from cc_daemon import schema

@pytest.fixture(autouse=True)
def _isolated(tmp_path: Path, monkeypatch):
    """Each test gets a private sessions.db."""
    schema.set_db_path(tmp_path / "sessions.db")
    schema._local.conn = None
    yield
    schema._local.conn = None
    schema.set_db_path(schema.get_default_db_path())

# ── CRUD ────────────────────────────────────────────────────────────────────

def test_add_then_list_returns_subscription():
    store.add_subscription("arxiv", schedule="daily", channels=["console"])
    subs = store.list_subscriptions()
    assert len(subs) == 1
    assert subs[0]["topic"] == "arxiv"
    assert subs[0]["schedule"] == "daily"
    assert subs[0]["channels"] == ["console"]

def test_add_is_upsert():
    store.add_subscription("arxiv", schedule="daily", channels=["console"])
    store.add_subscription("arxiv", schedule="6h", channels=["telegram"])
    subs = store.list_subscriptions()
    assert len(subs) == 1
    assert subs[0]["schedule"] == "6h"
    assert subs[0]["channels"] == ["telegram"]

def test_get_subscription_returns_none_when_absent():
    assert store.get_subscription("nope") is None

def test_get_subscription_returns_match():
    store.add_subscription("arxiv", schedule="daily", channels=["console"])
    sub = store.get_subscription("arxiv")
    assert sub is not None
    assert sub["topic"] == "arxiv"

def test_remove_subscription_returns_true_when_removed():
    store.add_subscription("arxiv", schedule="daily")
    assert store.remove_subscription("arxiv") is True
    assert store.list_subscriptions() == []

def test_remove_subscription_returns_false_when_absent():
    assert store.remove_subscription("never-was") is False

def test_update_last_run_records_timestamp_and_preview():
    store.add_subscription("arxiv", schedule="daily")
    store.update_last_run("arxiv", "Today's findings: …" + "x" * 1000)
    sub = store.get_subscription("arxiv")
    assert sub["last_run"] is not None
    # last_report preview is ≤500 chars per legacy behaviour
    assert len(sub["last_report"]) <= 500

def test_subscription_persists_across_connections():
    """Drop and re-create the thread-local connection to mimic a fresh
    process reading the same DB."""
    store.add_subscription("arxiv", schedule="daily", channels=["console"])
    schema._local.conn = None  # drop conn → next call re-opens
    subs = store.list_subscriptions()
    assert any(s["topic"] == "arxiv" for s in subs)

# ── Reports ─────────────────────────────────────────────────────────────────

def test_save_report_returns_id_and_persists():
    store.add_subscription("arxiv", schedule="daily")
    rid = store.save_report("arxiv", "Today's digest", sent_to=["console"])
    assert rid
    reports = store.list_reports("arxiv")
    assert len(reports) == 1
    assert reports[0]["id"] == rid
    assert reports[0]["body"] == "Today's digest"
    assert reports[0]["sent_to"] == ["console"]

def test_list_reports_filters_by_topic():
    store.add_subscription("arxiv", schedule="daily")
    store.add_subscription("news", schedule="6h")
    store.save_report("arxiv", "A", sent_to=[])
    store.save_report("news", "N", sent_to=[])
    store.save_report("arxiv", "B", sent_to=[])
    arxiv_reports = store.list_reports("arxiv")
    assert {r["body"] for r in arxiv_reports} == {"A", "B"}

def test_list_reports_orders_newest_first():
    store.add_subscription("arxiv", schedule="daily")
    store.save_report("arxiv", "first", sent_to=[])
    store.save_report("arxiv", "second", sent_to=[])
    store.save_report("arxiv", "third", sent_to=[])
    reports = store.list_reports("arxiv")
    # Most recent first
    assert reports[0]["body"] == "third"
    assert reports[-1]["body"] == "first"
