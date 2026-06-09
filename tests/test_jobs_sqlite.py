"""F-2 tests for jobs.py — SQLite backing."""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import jobs
from cc_daemon import schema


@pytest.fixture(autouse=True)
def _isolated_db_and_jobs_path(tmp_path: Path, monkeypatch):
    """Each test gets a private sessions.db."""
    schema.set_db_path(tmp_path / "sessions.db")
    schema._local.conn = None
    yield
    schema._local.conn = None
    schema.set_db_path(schema.get_default_db_path())


# ── Roundtrip ──────────────────────────────────────────────────────────────

def test_create_persists_to_sqlite():
    j = jobs.create("hello world", source="test")
    conn = schema.get_conn()
    row = conn.execute(
        "SELECT id, prompt, status FROM jobs WHERE id=?", (j.id,)
    ).fetchone()
    assert row is not None
    assert row["prompt"] == "hello world"
    assert row["status"] == "queued"


def test_get_returns_persisted_job():
    j = jobs.create("foo", source="test")
    fetched = jobs.get(j.id)
    assert fetched is not None
    assert fetched.id == j.id
    assert fetched.prompt == "foo"


def test_lifecycle_updates_status_in_sqlite():
    j = jobs.create("lifecycle", source="test")
    jobs.start(j.id)
    assert jobs.get(j.id).status == "running"
    jobs.complete(j.id, result_preview="done")
    assert jobs.get(j.id).status == "done"


def test_steps_are_round_tripped_as_json():
    j = jobs.create("with steps", source="test")
    jobs.add_step(j.id, "Bash", "ls -la")
    jobs.finish_step(j.id, "Bash", "5 files")
    fetched = jobs.get(j.id)
    assert any(s.get("name") == "Bash" for s in fetched.steps)


def test_list_recent_orders_newest_first():
    j1 = jobs.create("one", source="t")
    j2 = jobs.create("two", source="t")
    j3 = jobs.create("three", source="t")
    recent = jobs.list_recent(10)
    assert [r.id for r in recent[:3]] == [j3.id, j2.id, j1.id]


def test_list_running_only_returns_running():
    j1 = jobs.create("a", source="t"); jobs.start(j1.id)
    j2 = jobs.create("b", source="t")  # stays queued
    j3 = jobs.create("c", source="t"); jobs.start(j3.id); jobs.complete(j3.id)
    running = jobs.list_running()
    assert {r.id for r in running} == {j1.id}


def test_max_jobs_pruning_keeps_recent():
    """The legacy JSON storage capped at 100; SQLite mirror should too."""
    original = jobs._MAX_JOBS
    try:
        jobs._MAX_JOBS = 5
        for i in range(10):
            jobs.create(f"job-{i}", source="t")
        recent = jobs.list_recent(20)
        assert len(recent) == 5
        # Newest 5 survived
        assert [r.prompt for r in recent] == [f"job-{i}" for i in (9, 8, 7, 6, 5)]
    finally:
        jobs._MAX_JOBS = original

