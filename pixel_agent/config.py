"""Configuration loading for PIXEL — reads .env and exposes simple settings."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root if present
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

APP_DIR = Path.home() / ".pixel-agent"
APP_DIR.mkdir(exist_ok=True)

DB_PATH = APP_DIR / "pixel.db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# minimal | warm | witty — change anytime, no code changes needed
PERSONALITY = os.getenv("PIXEL_PERSONALITY", "warm")

# alias name -> real command/path, used by `pixel open` / `pixel run`
ALIASES = {
    "vscode": os.getenv("PIXEL_ALIAS_VSCODE", "code ."),
}
