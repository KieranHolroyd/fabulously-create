"""AST nodes and layout helpers for the Fabulously Create quest book."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .text import goal


@dataclass(frozen=True)
class ItemReward:
    item: str
    count: int = 1


@dataclass(frozen=True)
class XpLevels:
    levels: int = 1


@dataclass
class Quest:
    n: int
    x: float
    y: float
    task: str
    title: str
    desc: list[str]
    task_count: int = 1
    deps: list[int] = field(default_factory=list)
    # Cross-chapter hard dependencies (absolute quest numbers). Prefer
    # `require()` / chapter `links=` — visible Quest Links are wired from these.
    links: list[int] = field(default_factory=list)
    rewards: list[ItemReward | XpLevels] = field(default_factory=list)
    optional: bool = False
    size: float = 1.0
    shape: str | None = None
    subtitle: str = ""
    hide_until_deps: bool = False


@dataclass
class QuestLink:
    """Visual FTB Quest Link to a quest owned by another chapter."""

    linked: int  # absolute quest number
    x: float
    y: float
    size: float = 1.25
    shape: str | None = "pentagon"
    id: str = ""  # filled by wire_connections / compile if empty


@dataclass
class Chapter:
    key: str
    base: int
    chapter_id: str
    icon: str
    title: str
    subtitle: str
    quests: list[Quest]
    quest_links: list[QuestLink] = field(default_factory=list)


@dataclass
class Book:
    chapters: list[Chapter]


def require(*absolute_quest_numbers: int) -> list[int]:
    """Cross-chapter dependency list for `Quest(links=require(...))`."""
    return list(absolute_quest_numbers)


def connected(
    absolute: int,
    x: float,
    y: float,
    *,
    size: float = 1.25,
    shape: str | None = "pentagon",
) -> QuestLink:
    """Manual visual bridge to another chapter's quest."""
    return QuestLink(linked=absolute, x=x, y=y, size=size, shape=shape)


# Step tuple used by linear tech chapters:
# (n, task, title, count, what, body, tip, subtitle, dep)
Step = tuple[int, str, str, int, str, str, str, str, int | None]


def item(item_id: str, count: int = 1) -> ItemReward:
    return ItemReward(item_id, count)


def xp_levels(n: int = 1) -> XpLevels:
    return XpLevels(n)


def step_row(
    steps: Sequence[Step],
    *,
    y: float,
    cols: int = 10,
    link_first: int | None = None,
    size_at: set[int] | None = None,
    shape_at: set[int] | None = None,
    xp_from: int | None = None,
    subtitle_prefix: str = "",
) -> list[Quest]:
    """Lay out step tuples on a grid as Quest nodes."""
    size_at = size_at or set()
    shape_at = shape_at or set()
    first_n = steps[0][0]
    out: list[Quest] = []
    for n, task, title, count, what, body, tip, subtitle, dep in steps:
        idx = n - first_n
        out.append(
            Quest(
                n=n,
                x=(idx % cols) * 2.5,
                y=y + (idx // cols) * 2.5,
                task=task,
                title=title,
                desc=goal(what, body, tip=tip),
                task_count=count,
                deps=[dep] if dep is not None else [],
                links=[link_first] if n == first_n and link_first is not None else [],
                rewards=[xp_levels(2 if xp_from is not None and n >= xp_from else 1)],
                size=1.5 if n in size_at else 1.0,
                shape="hexagon" if n in shape_at else None,
                subtitle=f"{subtitle_prefix}{subtitle}" if subtitle_prefix else subtitle,
            )
        )
    return out

