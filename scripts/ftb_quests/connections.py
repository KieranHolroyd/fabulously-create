"""Connected quests (FTB Quest Links) and cross-chapter bridge helpers.

FTB Quests can show another chapter's quest inside the current chapter via
`quest_links`. That gives players a clickable, line-connected bridge instead of
an invisible cross-chapter dependency.

`Quest.links` remains the hard dependency (absolute quest numbers).
`Chapter.quest_links` / auto-wiring below is the visible connection.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace

from .ast import Book, Chapter, Quest, QuestLink
from .ids import quest_id


def stable_link_id(chapter_key: str, linked_absolute: int, x: float, y: float) -> str:
    """Deterministic 16-hex id for a quest_link entry.

    FTB Quests ids are parsed as signed 64-bit longs; a leading hex digit of
    8-F overflows Long.MAX_VALUE and gets silently discarded/regenerated at
    load. Force the leading nibble into 0-7.
    """
    payload = f"{chapter_key}:{linked_absolute}:{x:.3f}:{y:.3f}".encode()
    digest = hashlib.md5(payload).hexdigest()[:16].upper()
    return format(int(digest, 16) & 0x7FFFFFFFFFFFFFFF, "016X")


def page_link(absolute: int, label: str) -> str:
    """SNBT/lang line: yellow underlined jump to another quest."""
    return json.dumps(
        {
            "text": label,
            "color": "yellow",
            "underlined": True,
            "clickEvent": {"action": "change_page", "value": quest_id(absolute)},
        },
        separators=(",", ":"),
    )


@dataclass(frozen=True)
class Bridge:
    """Declare that a chapter should visually connect to an absolute quest id."""

    absolute: int
    x: float
    y: float
    size: float = 1.25
    shape: str | None = "pentagon"


def quest_link_from_bridge(chapter_key: str, bridge: Bridge) -> QuestLink:
    return QuestLink(
        linked=bridge.absolute,
        x=bridge.x,
        y=bridge.y,
        size=bridge.size,
        shape=bridge.shape,
        id=stable_link_id(chapter_key, bridge.absolute, bridge.x, bridge.y),
    )


def _title_index(book: Book) -> dict[int, str]:
    titles: dict[int, str] = {}
    for chapter in book.chapters:
        for quest in chapter.quests:
            titles[chapter.base + quest.n] = quest.title
    return titles


def _append_connection_blurb(quest: Quest, titles: dict[int, str]) -> Quest:
    """Add clickable 'Connected:' lines for cross-chapter requirements."""
    if not quest.links:
        return quest
    extra: list[str] = ["", "&6Connected:&r"]
    for absolute in quest.links:
        label = titles.get(absolute, f"Quest {absolute}")
        extra.append(page_link(absolute, f"→ {label}"))
    # Avoid duplicating if wire_connections runs twice
    if any(line.startswith("&6Connected:&r") for line in quest.desc):
        return quest
    return replace(quest, desc=[*quest.desc, *extra])


def wire_connections(book: Book) -> Book:
    """Attach Quest Links + description jumps for every cross-chapter `links=`."""
    titles = _title_index(book)
    chapters: list[Chapter] = []
    for chapter in book.chapters:
        # First quest that requires each absolute id wins the visual slot.
        bridges: dict[int, Bridge] = {}
        for quest in chapter.quests:
            for absolute in quest.links:
                if absolute in bridges:
                    continue
                bridges[absolute] = Bridge(
                    absolute=absolute,
                    x=quest.x - 2.5,
                    y=quest.y,
                )

        auto_links = [
            quest_link_from_bridge(chapter.key, bridge) for bridge in bridges.values()
        ]
        # Manual links win on exact (linked, x, y); otherwise append autos.
        manual = list(chapter.quest_links)
        manual_keys = {(ql.linked, round(ql.x, 3), round(ql.y, 3)) for ql in manual}
        for ql in auto_links:
            key = (ql.linked, round(ql.x, 3), round(ql.y, 3))
            if key not in manual_keys:
                if not ql.id:
                    ql = replace(
                        ql,
                        id=stable_link_id(chapter.key, ql.linked, ql.x, ql.y),
                    )
                manual.append(ql)

        wired_quests = [_append_connection_blurb(q, titles) for q in chapter.quests]
        chapters.append(
            replace(chapter, quests=wired_quests, quest_links=manual)
        )
    return Book(chapters=chapters)
