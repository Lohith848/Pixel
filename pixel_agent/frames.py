"""Pixel-art frames for the agent's states.

Each state maps to a list of frames (multi-line strings). States with more
than one frame animate by cycling through them; single-frame states are
static. Keep frames small so they never overwhelm a small terminal window.
"""

IDLE = [
    r"""
 ▄▄▄▄▄▄▄
 █ ■ ■ █
 █  ▽  █
 ▀▀▀▀▀▀▀
""",
    r"""
 ▄▄▄▄▄▄▄
 █ ─ ─ █
 █  ▽  █
 ▀▀▀▀▀▀▀
""",
]

THINKING = [
    r"""
 ▄▄▄▄▄▄▄
 █ ● ○ █
 █  ~  █
 ▀▀▀▀▀▀▀
   .
""",
    r"""
 ▄▄▄▄▄▄▄
 █ ○ ● █
 █  ~  █
 ▀▀▀▀▀▀▀
   ..
""",
    r"""
 ▄▄▄▄▄▄▄
 █ ● ○ █
 █  ~  █
 ▀▀▀▀▀▀▀
   ...
""",
]

TALKING = [
    r"""
 ▄▄▄▄▄▄▄
 █ ■ ■ █
 █  ▼  █
 ▀▀▀▀▀▀▀
""",
]

ERROR = [
    r"""
 ▄▄▄▄▄▄▄
 █ ✕ ✕ █
 █  ︵  █
 ▀▀▀▀▀▀▀
""",
]

CELEBRATING = [
    r"""
 ✦ ▄▄▄▄▄▄▄ ✦
   █ ^ ^ █
   █  ▽  █
   ▀▀▀▀▀▀▀
""",
]

STATES = {
    "idle": IDLE,
    "thinking": THINKING,
    "talking": TALKING,
    "error": ERROR,
    "celebrating": CELEBRATING,
}


def get_frame(state: str, tick: int = 0) -> str:
    frames = STATES.get(state, IDLE)
    return frames[tick % len(frames)]
