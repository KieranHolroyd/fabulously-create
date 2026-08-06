"""Compile Book AST into the quest/lang dicts consumed by the SNBT writer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast import Book, Chapter, ItemReward, Quest, QuestLink, XpLevels
from .connections import stable_link_id
from .ids import quest_id


def _corrected_x(chapter: Chapter, step: float = 2.5) -> dict[int, float]:
    """Push quests right until dependency lines flow forward and rows don't collide.

    Hand-authored x/y sometimes places a quest to the left of a quest it
    depends on (a branch row restarting its x near the chapter's start).
    FTB Quests draws a straight dependency line between quest centers, so
    that reads as an arrow pointing backwards and crosses over unrelated
    nodes.

    Two constraints are relaxed to a fixed point:
      1. x(quest) >= x(dependency) + step, for every same-chapter dep.
      2. Within a row (same y), quests keep their authored left-to-right
         order but are spread out by at least `step` so a dependency push
         can't stack two of them on the same spot.
    x only ever increases; y (lane/row grouping) is never touched.
    """
    by_n = {q.n: q for q in chapter.quests}
    x = {q.n: q.x for q in chapter.quests}

    rows: dict[float, list[int]] = {}
    for q in chapter.quests:
        rows.setdefault(q.y, []).append(q.n)
    for row in rows.values():
        row.sort(key=lambda n: by_n[n].x)

    for _ in range(len(chapter.quests) + 1):
        changed = False
        for q in chapter.quests:
            for dep_n in q.deps:
                dep_q = by_n.get(dep_n)
                if dep_q is None:
                    continue
                floor = x[dep_n] + step
                if x[q.n] < floor:
                    x[q.n] = floor
                    changed = True
        for row in rows.values():
            for prev_n, n in zip(row, row[1:]):
                floor = x[prev_n] + step
                if x[n] < floor:
                    x[n] = floor
                    changed = True
        if not changed:
            break

    return x


def _rewards_to_dicts(quest: Quest) -> list[dict[str, Any]] | None:
    if not quest.rewards:
        return None
    out: list[dict[str, Any]] = []
    for reward in quest.rewards:
        if isinstance(reward, ItemReward):
            out.append({"type": "item", "item": reward.item, "count": reward.count})
        elif isinstance(reward, XpLevels):
            out.append({"type": "xp_levels", "xp_levels": reward.levels})
        else:
            raise TypeError(f"unknown reward type: {type(reward)!r}")
    return out


def compile_quest(
    chapter: Chapter, quest: Quest, x_by_n: dict[int, float]
) -> tuple[dict[str, Any], dict[str, Any]]:
    absolute = chapter.base + quest.n
    qid = quest_id(absolute)
    dep_ids = [quest_id(chapter.base + i) for i in quest.deps] + [
        quest_id(i) for i in quest.links
    ]
    seen: set[str] = set()
    ordered: list[str] = []
    for dep in dep_ids:
        if dep not in seen:
            seen.add(dep)
            ordered.append(dep)
    meta = {
        "id": qid,
        "x": x_by_n[quest.n],
        "y": quest.y,
        "task": quest.task,
        "task_count": quest.task_count,
        "rewards": _rewards_to_dicts(quest),
        "deps": ordered,
        "optional": quest.optional,
        "size": quest.size,
        "shape": quest.shape,
        "hide_until_deps": quest.hide_until_deps,
    }
    lang = {
        "title": quest.title,
        "desc": quest.desc,
        "subtitle": quest.subtitle,
    }
    return meta, lang


def compile_quest_link(chapter: Chapter, link: QuestLink) -> dict[str, Any]:
    link_id = link.id or stable_link_id(chapter.key, link.linked, link.x, link.y)
    meta: dict[str, Any] = {
        "id": link_id,
        "linked_quest": quest_id(link.linked),
        "x": link.x,
        "y": link.y,
        "size": link.size,
    }
    if link.shape:
        meta["shape"] = link.shape
    return meta


@dataclass
class CompiledChapter:
    key: str
    chapter_id: str
    icon: str
    title: str
    subtitle: str
    quests: list[dict[str, Any]]
    lang: dict[str, dict[str, Any]]
    quest_links: list[dict[str, Any]]


def compile_chapter(chapter: Chapter) -> CompiledChapter:
    x_by_n = _corrected_x(chapter)
    quests_meta: list[dict[str, Any]] = []
    lang_map: dict[str, dict[str, Any]] = {}
    for quest in chapter.quests:
        meta, lang = compile_quest(chapter, quest, x_by_n)
        quests_meta.append(meta)
        lang_map[meta["id"]] = lang
    return CompiledChapter(
        key=chapter.key,
        chapter_id=chapter.chapter_id,
        icon=chapter.icon,
        title=chapter.title,
        subtitle=chapter.subtitle,
        quests=quests_meta,
        lang=lang_map,
        quest_links=[compile_quest_link(chapter, ql) for ql in chapter.quest_links],
    )


def compile_book(book: Book) -> dict[str, CompiledChapter]:
    """Return an ordered mapping of chapter key → compiled chapter."""
    return {chapter.key: compile_chapter(chapter) for chapter in book.chapters}
