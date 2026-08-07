"""Synthesize a click-to-complete "chapter start" quest per chapter."""
from __future__ import annotations

from dataclasses import replace

from .ast import Book, Chapter, Quest, xp_levels

# Absolute quest number ranges are packed tight — some chapters' last quest
# directly abuts the next chapter's first (e.g. storage_gear ends at 323,
# refined_storage starts at 324). A small negative `n` like -1 would collide
# with the previous chapter's last quest id. This sentinel offset keeps
# every synthesized intro's absolute number (chapter.base + n) safely above
# every authored quest number, while staying unique per chapter since each
# chapter's base is unique.
INTRO_N = 90000

FOUNDATIONS_KEY = "foundations"


def _chapter_name(title: str) -> str:
    """Strip the leading "N. " numbering from a chapter title."""
    _, _, rest = title.partition(". ")
    return rest or title


def add_chapter_intros(book: Book) -> Book:
    """Give every chapter a checkmark quest at the very start.

    `foundations` already opens with a welcome quest, so it's converted to
    checkmark in place rather than getting a second intro. Every other
    chapter gets a new checkmark quest inserted before its first (real,
    item-gated) quest, which gains a dependency on it.
    """
    chapters: list[Chapter] = []
    for chapter in book.chapters:
        first = min(chapter.quests, key=lambda q: q.n)

        if chapter.key == FOUNDATIONS_KEY:
            quests = [
                replace(q, checkmark=True) if q.n == first.n else q
                for q in chapter.quests
            ]
            chapters.append(replace(chapter, quests=quests))
            continue

        intro = Quest(
            n=INTRO_N,
            x=first.x - 2.5,
            y=first.y,
            task=first.task,
            title=f"Welcome to {_chapter_name(chapter.title)}",
            desc=[
                chapter.subtitle,
                "",
                "&7Click the checkbox to mark this complete and dive in.&r",
            ],
            checkmark=True,
            rewards=[xp_levels(1)],
        )
        quests = [
            replace(q, deps=[*q.deps, INTRO_N]) if q.n == first.n else q
            for q in chapter.quests
        ]
        chapters.append(replace(chapter, quests=[intro, *quests]))
    return Book(chapters=chapters)
