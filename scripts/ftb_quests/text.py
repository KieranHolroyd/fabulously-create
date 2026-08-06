"""Quest description helpers."""
from __future__ import annotations


def goal(
    what: str,
    *body: str,
    tip: str | None = None,
    nxt: str | None = None,
) -> list[str]:
    """Standard quest blurb: Goal → why → tip → next."""
    lines: list[str] = [f"&6Goal:&r {what}", ""]
    for para in body:
        lines.append(para)
        lines.append("")
    if tip:
        lines.append(f"&7Tip:&r {tip}")
    if nxt:
        lines.append(f"&7Next:&r {nxt}")
    while lines and lines[-1] == "":
        lines.pop()
    return lines
