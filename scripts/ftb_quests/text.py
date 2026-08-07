"""Quest description helpers — tutorial-first formatting."""
from __future__ import annotations

from collections.abc import Sequence


def _blank_join(parts: Sequence[str]) -> list[str]:
    """Join description paragraphs with readable spacer rows."""
    lines: list[str] = []
    for part in parts:
        if lines:
            lines.append("")
        lines.append(part)
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

    Structure:
      Goal → Why → up to two numbered actions → Caution → Tip

    Item tasks remain the checkpoint; the numbered actions teach the build.
    """
    parts: list[str] = [f"&6Goal:&r {what}"]
    if why:
        parts.append(why)
    if steps:
        # Two actions fit in the panel and cover the useful path. In longer
        # checklists the goal already says what to craft, so retain the two
        # central setup/use actions instead of repeating the recipe errand.
        selected_steps = steps[1:3] if len(steps) > 3 else steps[:2]
        how_lines = ["&6How:&r"]
        for i, step in enumerate(selected_steps, start=1):
            how_lines.append(f"&e{i}.&r {step}")
        parts.append("\n".join(how_lines))
    if caution:
        parts.append(f"&cCaution:&r {caution}")
    if tip:
        parts.append(f"&7Tip:&r {tip}")
    # Dependencies and quest links already show the next step. `nxt` remains
    # accepted so older chapter definitions stay source-compatible, but the
    # repeated navigation sentence is intentionally omitted from the panel.
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
