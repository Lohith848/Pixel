
## PIXEL — Your Terminal AI Assistant

PIXEL is a clever, pixel-art CLI assistant that lives directly in your terminal. It helps you manage notes, track to-dos, set reminders, execute terminal commands, and chat with AI — all backed by the lightning-fast Groq API with a customizable personality.

Everything except free-text AI chat works completely offline, and all your data is stored locally.

### Features

- Conversational AI — Chat with PIXEL directly from your terminal.
- Mood System — Change PIXEL's personality on the fly ("normal", "focused", "debugging", "roast").
- Terminal Execution — Ask PIXEL to generate and safely execute shell commands.
- Task Management — Fully offline notes, to-dos, and reminders.
- Aliases — Configure shortcuts to open apps or run frequently used scripts.
- Global Terminal Access — Install PIXEL with "pipx" and use the "pixel" command from any directory without manually activating a virtual environment.

---

### Installation

1. Clone the repository

git clone https://github.com/Lohith848/Pixel.git
cd Pixel

2. Configure your Groq API key

Copy the example environment file:

copy .env.example .env

Open ".env" and add your Groq API key.

---

## Recommended: Global Installation with pipx

Using "pipx" allows PIXEL to live directly in your terminal.

You won't need to navigate to the PIXEL folder or activate a virtual environment every time you want to use it.

1. Install pipx

py -m pip install --user pipx

2. Add pipx to PATH

py -m pipx ensurepath

Close and reopen PowerShell after running this command.

Verify the installation:

pipx --version

3. Install PIXEL globally

From inside the PIXEL repository:

pipx install -e .

The "-e" flag installs PIXEL in editable mode, which is useful for development. Changes you make to PIXEL's Python source code will be reflected without having to reinstall the package every time.

4. Run PIXEL from anywhere

You can now leave the project directory:

cd $HOME

And simply run:

pixel look

Or:

pixel "hello"

PIXEL is now available globally in your terminal.

No more:

cd Downloads
cd pixel-agent
.\venv\Scripts\activate

Just:

pixel

---

## Alternative: Virtual Environment Installation

If you don't want to install PIXEL globally, you can still use a traditional Python virtual environment.

Create the environment:

python -m venv venv

Activate it on Windows:

.\venv\Scripts\activate

Install PIXEL:

pip install -e .

PIXEL will then be available while the virtual environment is active.

---

## Usage Guide

# AI and Execution

Chat with PIXEL:

pixel "what is my schedule?"

Ask PIXEL to generate a terminal command:

pixel do "find all python files"

PIXEL generates the appropriate command and asks for confirmation before executing it.

Change PIXEL's personality:

pixel mood roast

Available moods:

normal
focused
debugging
roast

---

## Offline Utilities

Display PIXEL's mascot:

pixel look

Add a note:

pixel note "idea: build a terminal game"

View your notes:

pixel note list

Add a to-do:

pixel todo add "fix login bug"

View open to-dos:

pixel todo list

View all to-dos:

pixel todo list --all

Mark a to-do as complete:

pixel todo done <id>

Add a reminder:

pixel remind "call mom" --at "6pm"

View pending reminders:

pixel remind list

---

### Custom Aliases

PIXEL can run aliases configured in your ".env" file.

For example:

pixel open vscode

This lets you create shortcuts for frequently used applications, commands, or scripts.

---

### Example

Once PIXEL is globally installed, you can open a fresh PowerShell window from any directory:

PS C:\Users\User> pixel look

╭──── PIXEL ────╮
│               │
│  ▄▄▄▄▄▄▄      │
│  █ ■ ■ █      │
│  █  ▽  █      │
│  ▀▀▀▀▀▀▀      │
│               │
│  "your move." │
╰───────────────╯

Then simply talk to it:

pixel "explain recursion"

PIXEL stays one command away — wherever you are in your terminal.


### Author

LOHITH G
