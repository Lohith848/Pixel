"""Local SQLite storage — notes, todos, reminders, command_log.

Everything here works fully offline. No network, no API keys required.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    remind_at TEXT NOT NULL,
    delivered INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS command_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_db() as db:
        db.executescript(SCHEMA)


def log_command(command: str) -> None:
    with get_db() as db:
        db.execute(
            "INSERT INTO command_log (command, created_at) VALUES (?, ?)",
            (command, datetime.now().isoformat()),
        )


def get_recent_commands(limit: int = 6) -> list[str]:
    """Return the most recent commands to provide AI context."""
    with get_db() as db:
        rows = db.execute(
            "SELECT command FROM command_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        # reverse so chronological order
        return [r["command"] for r in reversed(rows)]


# ---------- Settings ----------
def get_setting(key: str, default: str = "") -> str:
    with get_db() as db:
        row = db.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if row:
            return row["value"]
        return default


def set_setting(key: str, value: str) -> None:
    with get_db() as db:
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value)
        )


# ---------- Notes ----------
def add_note(text: str) -> int:
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO notes (text, created_at) VALUES (?, ?)",
            (text, datetime.now().isoformat()),
        )
        return cur.lastrowid


def list_notes(limit: int = 20) -> list[sqlite3.Row]:
    with get_db() as db:
        return db.execute(
            "SELECT * FROM notes ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()


# ---------- Todos ----------
def add_todo(text: str) -> int:
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO todos (text, created_at) VALUES (?, ?)",
            (text, datetime.now().isoformat()),
        )
        return cur.lastrowid


def list_todos(include_done: bool = False) -> list[sqlite3.Row]:
    with get_db() as db:
        if include_done:
            return db.execute("SELECT * FROM todos ORDER BY id").fetchall()
        return db.execute(
            "SELECT * FROM todos WHERE done = 0 ORDER BY id"
        ).fetchall()


def complete_todo(todo_id: int) -> bool:
    with get_db() as db:
        cur = db.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
        return cur.rowcount > 0


# ---------- Reminders ----------
def add_reminder(text: str, remind_at: str) -> int:
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO reminders (text, remind_at, created_at) VALUES (?, ?, ?)",
            (text, remind_at, datetime.now().isoformat()),
        )
        return cur.lastrowid


def list_reminders(include_delivered: bool = False) -> list[sqlite3.Row]:
    with get_db() as db:
        if include_delivered:
            return db.execute("SELECT * FROM reminders ORDER BY remind_at").fetchall()
        return db.execute(
            "SELECT * FROM reminders WHERE delivered = 0 ORDER BY remind_at"
        ).fetchall()


def due_reminders(now_iso: str) -> list[sqlite3.Row]:
    with get_db() as db:
        return db.execute(
            "SELECT * FROM reminders WHERE delivered = 0 AND remind_at <= ?",
            (now_iso,),
        ).fetchall()


def mark_delivered(reminder_id: int) -> None:
    with get_db() as db:
        db.execute("UPDATE reminders SET delivered = 1 WHERE id = ?", (reminder_id,))
