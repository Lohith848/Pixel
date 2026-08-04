"""PIXEL — a pixel-art CLI agent for daily-life commands.

Run `pixel --help` to see everything. Structured commands (note/todo/remind/
open/run/look) work fully offline. Free text is routed to the AI layer.
"""
from __future__ import annotations

import random
import subprocess
import sys
from typing import List, Optional

import typer
from dateutil import parser as dateparser

if sys.platform == "win32" and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from . import ai, render, storage
from .config import ALIASES, PERSONALITY

app = typer.Typer(add_completion=False, no_args_is_help=False)
todo_app = typer.Typer(no_args_is_help=True)
app.add_typer(todo_app, name="todo", help="Manage your todo list.")

storage.init_db()

# Known top-level command names. A Typer/Click *group* can't mix a catch-all
# positional argument with named subcommands (the catch-all greedily eats the
# subcommand name first) — so free text is routed to an explicit `chat`
# command instead, via the argv rewrite in run() below.
KNOWN_COMMANDS = {"look", "note", "todo", "remind", "open", "run", "chat", "mood", "do"}

GREETINGS = {
    "minimal": ["ready.", "listening.", "go ahead."],
    "warm": ["hey! what's up?", "here for you \u2014 what do you need?", "ready when you are."],
    "witty": ["still standing by, unlike your build.", "beep. boop. i mean, hi.", "your move.", "now its not important","I'm here"],
}


def _greeting() -> str:
    return random.choice(GREETINGS.get(PERSONALITY, GREETINGS["warm"]))


# ---------------- look ----------------
@app.command()
def look():
    """Show the pixel agent."""
    render.show("idle", _greeting())


# ---------------- note ----------------
@app.command()
def note(words: List[str] = typer.Argument(..., help='Note text, or "list" to view notes')):
    """Add a note, or `pixel note list` to view recent notes."""
    if len(words) == 1 and words[0].lower() == "list":
        rows = storage.list_notes()
        if not rows:
            render.show("idle", "no notes yet.")
            return
        lines = "\n".join(f"[{r['id']}] {r['text']}" for r in rows)
        typer.echo(lines)
        render.show("talking", f"{len(rows)} note(s) on file.")
        return

    text = " ".join(words)
    storage.add_note(text)
    storage.log_command(f"note {text}")
    render.show("celebrating", "noted!")


# ---------------- todo ----------------
@todo_app.command("add")
def todo_add(text: List[str] = typer.Argument(...)):
    """Add a todo item."""
    joined = " ".join(text)
    storage.add_todo(joined)
    storage.log_command(f"todo add {joined}")
    render.show("celebrating", "added to your list!")


@todo_app.command("list")
def todo_list(all: bool = typer.Option(False, "--all", help="Include completed items")):
    """List open todos (or all, with --all)."""
    rows = storage.list_todos(include_done=all)
    if not rows:
        render.show("idle", "nothing on your list \u2014 nice.")
        return
    for r in rows:
        mark = "x" if r["done"] else " "
        typer.echo(f"[{mark}] {r['id']}: {r['text']}")
    render.show("talking", f"{len(rows)} item(s) shown.")


@todo_app.command("done")
def todo_done(todo_id: int):
    """Mark a todo as done by its id."""
    ok = storage.complete_todo(todo_id)
    if ok:
        render.show("celebrating", f"todo {todo_id} done \u2014 nice work.")
    else:
        render.show("error", f"couldn't find todo {todo_id}.")


# ---------------- remind ----------------
@app.command()
def remind(
    words: List[str] = typer.Argument(..., help='Reminder text, or "list" to view reminders'),
    at: Optional[str] = typer.Option(None, "--at", help="When to remind you, e.g. '6pm', '2026-08-10 09:00'"),
):
    """Add a reminder with --at, or `pixel remind list` to view them."""
    if len(words) == 1 and words[0].lower() == "list":
        rows = storage.list_reminders()
        if not rows:
            render.show("idle", "no reminders pending.")
            return
        lines = "\n".join(f"[{r['id']}] {r['text']} @ {r['remind_at']}" for r in rows)
        typer.echo(lines)
        render.show("talking", f"{len(rows)} reminder(s) pending.")
        return

    if not at:
        render.show("error", "add --at \"<time>\" so I know when to remind you.")
        raise typer.Exit(code=1)

    try:
        when = dateparser.parse(at, fuzzy=True)
    except (ValueError, OverflowError):
        render.show("error", f"couldn't understand the time '{at}'.")
        raise typer.Exit(code=1)

    text = " ".join(words)
    storage.add_reminder(text, when.isoformat())
    storage.log_command(f"remind {text} at {at}")
    render.show("celebrating", f"i'll remind you: {when.strftime('%b %d, %I:%M %p')}")


# ---------------- open / run ----------------
@app.command()
def open(alias: str):
    """Open an app by its configured alias (see .env / config.py ALIASES)."""
    cmd = ALIASES.get(alias)
    if not cmd:
        render.show("error", f"no alias '{alias}' configured yet.")
        raise typer.Exit(code=1)
    subprocess.Popen(cmd, shell=True)
    render.show("talking", f"opening {alias}...")


@app.command()
def run(alias: str):
    """Run a configured script/command alias."""
    cmd = ALIASES.get(alias)
    if not cmd:
        render.show("error", f"no alias '{alias}' configured yet.")
        raise typer.Exit(code=1)
    subprocess.run(cmd, shell=True)
    render.show("talking", f"ran {alias}.")


# ---------------- mood / do ----------------
@app.command()
def mood(mode: Optional[str] = typer.Argument(None)):
    """Set or view the current mood (normal, focused, debugging, roast)."""
    if not mode:
        current = storage.get_setting("mood", "normal")
        render.show("talking", f"I'm currently in {current.upper()} mode.")
        return
    valid_modes = {"normal", "focused", "debugging", "roast"}
    mode = mode.lower()
    if mode not in valid_modes:
        render.show("error", f"Unknown mood '{mode}'. Valid modes: {', '.join(valid_modes)}")
        return
    storage.set_setting("mood", mode)
    render.show("celebrating", f"Mood set to {mode.upper()}.")


@app.command("do")
def do_cmd(text: List[str] = typer.Argument(...)):
    """Ask PIXEL to generate and execute a terminal command."""
    query = " ".join(text)
    storage.log_command(f"do {query}")
    
    cmd_str = render.animate_task("thinking", lambda: ai.ask_for_command(query))
    if not cmd_str:
        render.show("error", "I couldn't generate a command right now.")
        return
        
    render.show("talking", f"Proposed command:\n  {cmd_str}")
    if typer.confirm("Do you want me to run this?"):
        render.show("celebrating", "Executing...")
        subprocess.run(cmd_str, shell=True)
    else:
        render.show("idle", "Canceled.")


# ---------------- free-text chat ----------------
@app.command()
def chat(text: Optional[List[str]] = typer.Argument(None)):
    """Talk to PIXEL directly — this is also where bare free text ends up."""
    if not text:
        render.show("idle", _greeting())
        return

    query = " ".join(text)
    storage.log_command(query)
    reply = render.animate_task("thinking", lambda: ai.ask(query))
    render.show("talking", reply)


def run():
    """Console-script entrypoint. Rewrites bare free text to `chat ...` so
    Click's group/subcommand resolution never has to fight a catch-all arg."""
    argv = sys.argv[1:]
    if not argv or (argv[0] not in KNOWN_COMMANDS and not argv[0].startswith("-")):
        sys.argv = [sys.argv[0], "chat", *argv]
    app()


if __name__ == "__main__":
    run()
