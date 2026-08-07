"""Structural validation for the authored quest book."""
from __future__ import annotations

from collections import Counter

from .ast import Book


def validate_book(book: Book) -> None:
    """Reject broken links, duplicate ids, and unusable quest copy."""
    absolute_ids = [
        chapter.base + quest.n
        for chapter in book.chapters
        for quest in chapter.quests
    ]
    duplicates = sorted(qid for qid, count in Counter(absolute_ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"duplicate absolute quest ids: {duplicates}")

    known = set(absolute_ids)
    errors: list[str] = []
    for chapter in book.chapters:
        local = {quest.n for quest in chapter.quests}
        for quest in chapter.quests:
            absolute = chapter.base + quest.n
            missing_deps = sorted(set(quest.deps) - local)
            missing_links = sorted(set(quest.links) - known)
            if missing_deps:
                errors.append(f"{absolute}: missing local deps {missing_deps}")
            if missing_links:
                errors.append(f"{absolute}: missing linked quests {missing_links}")
            if quest.task_count < 1:
                errors.append(f"{absolute}: task count must be positive")
            if not quest.title.strip():
                errors.append(f"{absolute}: title is empty")
            if not quest.desc or not any(line.strip() for line in quest.desc):
                errors.append(f"{absolute}: description is empty")

    if errors:
        raise ValueError("invalid quest book:\n- " + "\n- ".join(errors))
