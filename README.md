# PIXEL — Your Terminal AI Assistant

PIXEL is a clever, pixel-art CLI assistant that lives directly in your terminal. It helps you manage notes, track to-dos, set reminders, and execute terminal commands, all backed by a lightning-fast AI (Groq) with a customizable personality.

Everything except free-text chat works completely offline, and all data is stored locally.

## Features

- **Conversational AI**: Chat with PIXEL right in your terminal.
- **Mood System**: Change PIXEL's personality on the fly (`normal`, `focused`, `debugging`, `roast`).
- **Terminal Execution**: Ask PIXEL to generate and execute shell commands for you safely.
- **Task Management**: Fully offline notes, to-dos, and reminders.
- **Aliases**: Configure short aliases to open apps or run frequent scripts.

## Installation

1. **Clone and setup the environment:**
   ```bash
   git clone https://github.com/Lohith848/Pixel.git
   cd Pixel
   python -m venv venv
   ```

2. **Activate the environment (Windows):**
   ```powershell
   .\venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Configuration:**
   Copy the example environment file and add your Groq API key:
   ```bash
   copy .env.example .env
   ```

After installation, the `pixel` command will be available anywhere in your active terminal.

## Usage Guide

### AI and Execution
- `pixel "what is my schedule?"` — Chat with PIXEL via AI.
- `pixel do "find all python files"` — PIXEL generates the command and asks if you want to run it.
- `pixel mood roast` — Change PIXEL's personality (`normal`, `focused`, `debugging`, `roast`).

### Offline Utilities
- `pixel look` — Display the mascot.
- `pixel note "idea: ..."` — Add a quick note.
- `pixel note list` — View your notes.
- `pixel todo add "fix login bug"` — Add a to-do item.
- `pixel todo list [--all]` — List open (or all) to-dos.
- `pixel todo done <id>` — Mark a to-do as complete.
- `pixel remind "call mom" --at "6pm"` — Add a reminder.
- `pixel remind list` — View pending reminders.

### Custom Aliases
- `pixel open vscode` — Run a configured alias (defined in your `.env`).
- `pixel run <alias>` — Run a configured script alias.

## Storage and Privacy

All your notes, to-dos, and reminders are stored locally in `~/.pixel-agent/pixel.db` using SQLite. No account is required, and your data never leaves your machine unless you are using the AI chat feature.
