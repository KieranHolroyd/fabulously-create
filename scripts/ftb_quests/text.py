"""Quest description helpers — tutorial-first formatting."""
from __future__ import annotations

from collections.abc import Sequence


def _blank_join(parts: Sequence[str]) -> list[str]:
    """Join paragraphs with blank lines; drop trailing empties."""
    lines: list[str] = []
    for para in parts:
        if lines:
            lines.append("")
        lines.append(para)
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def goal(
    what: str,
    *body: str,
    tip: str | None = None,
    nxt: str | None = None,
) -> list[str]:
    """Legacy blurb — prefer tutorial() for new / rewritten quests."""
    return tutorial(what, why=body[0] if body else None, steps=list(body[1:]) or None, tip=tip, nxt=nxt)


def tutorial(
    what: str,
    *,
    why: str | None = None,
    steps: Sequence[str] | None = None,
    caution: str | None = None,
    tip: str | None = None,
    nxt: str | None = None,
) -> list[str]:
    """Tutorial-style quest text used across the book.

    Structure (matches ATM / FTB tutorial packs):
      Goal → Why → How (numbered) → Caution → Tip → Next

    Item tasks remain the checkpoint; the How block teaches the build.
    """
    parts: list[str] = [f"&6Goal:&r {what}"]
    if why:
        parts.append(why)
    if steps:
        how_lines = ["&6How:&r"]
        for i, step in enumerate(steps, start=1):
            how_lines.append(f"&e{i}.&r {step}")
        parts.append("\n".join(how_lines))
    if caution:
        parts.append(f"&cCaution:&r {caution}")
    if tip:
        parts.append(f"&7Tip:&r {tip}")
    if nxt:
        parts.append(f"&7Next:&r {nxt}")
    return _blank_join(parts)


def overview(
    pitch: str,
    *,
    you_will: Sequence[str],
    tip: str | None = None,
) -> list[str]:
    """Chapter / branch intro: what this line teaches."""
    parts = [
        pitch,
        "&6You will:&r\n" + "\n".join(f"&e•&r {item}" for item in you_will),
    ]
    if tip:
        parts.append(f"&7Tip:&r {tip}")
    return _blank_join(parts)
