"""Renders the pixel agent using Rich — static frame or a brief live animation."""
from __future__ import annotations

import time

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.live import Live

from . import frames

console = Console()

STATE_COLORS = {
    "idle": "cyan",
    "thinking": "yellow",
    "talking": "green",
    "error": "red",
    "celebrating": "magenta",
}


def _panel(state: str, tick: int, line: str | None) -> Panel:
    art = frames.get_frame(state, tick)
    body = art if not line else f"{art}\n \"{line}\""
    color = STATE_COLORS.get(state, "cyan")
    return Panel(Align.center(body), border_style=color, title="PIXEL", expand=False)


def show(state: str, line: str | None = None) -> None:
    """Render a single static frame (used for quick, non-animated states)."""
    console.print(_panel(state, 0, line))


def animate_task(state: str, task, fps: float = 4.0, min_cycles: int = 4) -> any:
    """Animate a state while a background task runs, clearing when done."""
    import threading
    result = []
    done = []
    def worker():
        try:
            result.append(task())
        finally:
            done.append(True)
    
    t = threading.Thread(target=worker)
    t.start()
    
    delay = 1.0 / fps
    tick = 0
    with Live(_panel(state, 0, None), console=console, refresh_per_second=fps, transient=True) as live:
        while not done or tick < min_cycles:
            live.update(_panel(state, tick, None))
            tick += 1
            time.sleep(delay)
            
    t.join()
    return result[0]
