"""Compile Book AST into the quest/lang dicts consumed by the SNBT writer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast import Book, Chapter, ItemReward, Quest, QuestLink, XpLevels
from .connections import stable_link_id
from .ids import quest_id

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


def compile_quest(chapter: Chapter, quest: Quest) -> tuple[dict[str, Any], dict[str, Any]]:
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
        "x": quest.x,
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
    quests_meta: list[dict[str, Any]] = []
    lang_map: dict[str, dict[str, Any]] = {}
    for quest in chapter.quests:
        meta, lang = compile_quest(chapter, quest)
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
