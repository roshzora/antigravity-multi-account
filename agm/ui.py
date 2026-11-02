"""
Terminal UI, Unicode box-drawing tables, color badges, and formatting for agm.
"""

import os
import sys
from typing import Any, List, Optional

# ANSI Color Codes
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"


def is_color_enabled() -> bool:
    """Check if color should be rendered."""
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def colorize(text: Any, color: str) -> str:
    """Return text wrapped in color if enabled."""
    text_str = str(text)
    if not is_color_enabled():
        return text_str
    return f"{color}{text_str}{RESET}"


def badge(status_text: str) -> str:
    """Return a pretty color badge for account status."""
    st = status_text.lower()
    if "auto-refresh" in st:
        return colorize(f"● {status_text}", GREEN + BOLD)
    elif "active" in st:
        return colorize(f"● {status_text}", GREEN)
    elif "expired" in st:
        return colorize(f"⚠ {status_text}", RED + BOLD)
    elif "needs login" in st or "missing" in st:
        return colorize(f"○ {status_text}", YELLOW)
    elif "error" in st or "invalid" in st:
        return colorize(f"✖ {status_text}", RED)
    return status_text


def print_banner():
    """Print a clean CLI header banner."""
    banner = rf"""
{CYAN + BOLD}   ___    ____  __  ___
  / _ |  / ___//  |/  /
 / __ | / (_ // /|_/ / 
/_/ |_| \___//_/  /_/  {RESET}{DIM}Antigravity Multi-Account Manager v1.0.0{RESET}
{DIM}Simultaneous sessions, zero token collisions, automatic pooling.{RESET}
"""
    print(banner)


def render_table(headers: List[str], rows: List[List[str]], alignments: Optional[List[str]] = None):
    """
    Render a modern Unicode box-drawing table.
    Supports alignments: 'L' (left, default), 'R' (right), 'C' (center).
    """
    if not rows:
        return

    num_cols = len(headers)
    aligns = alignments or ["L"] * num_cols

    # Calculate max visible width for each column (stripping ANSI codes for length)
    import re
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def visible_len(s: str) -> int:
        return len(ansi_escape.sub("", str(s)))

    col_widths = [visible_len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], visible_len(cell))

    # Pad with 1 char margin on each side
    col_widths = [w + 2 for w in col_widths]

    def pad_cell(content: str, width: int, align: str) -> str:
        v_len = visible_len(content)
        extra = width - v_len - 2
        if extra < 0:
            extra = 0
        if align == "R":
            return " " + (" " * extra) + content + " "
        elif align == "C":
            left = extra // 2
            right = extra - left
            return " " + (" " * left) + content + (" " * right) + " "
        else:
            return " " + content + (" " * extra) + " "

    # Unicode border characters
    top_line = "┌" + "┬".join("─" * w for w in col_widths) + "┐"
    mid_line = "├" + "┼".join("─" * w for w in col_widths) + "┤"
    bot_line = "└" + "┴".join("─" * w for w in col_widths) + "┘"

    print(colorize(top_line, DIM))

    # Header row
    hdr_cells = [colorize(pad_cell(headers[i], col_widths[i], aligns[i]), BOLD) for i in range(num_cols)]
    print(colorize("│", DIM) + colorize("│", DIM).join(hdr_cells) + colorize("│", DIM))
    print(colorize(mid_line, DIM))

    # Data rows
    for row in rows:
        cells = []
        for i in range(num_cols):
            val = row[i] if i < len(row) else ""
            cells.append(pad_cell(val, col_widths[i], aligns[i]))
        print(colorize("│", DIM) + colorize("│", DIM).join(cells) + colorize("│", DIM))

    print(colorize(bot_line, DIM))


def print_step(step_num: int, total_steps: int, title: str):
    """Print a progress step."""
    prefix = colorize(f"[{step_num}/{total_steps}]", CYAN + BOLD)
    print(f"\n{prefix} {BOLD}{title}{RESET}")
