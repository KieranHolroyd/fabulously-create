"""Chapter registry — order here is the quest-book tab order."""
from __future__ import annotations

from ftb_quests.ast import Chapter

from . import (
    automation,
    create_factory,
    extreme_reactors,
    factory_challenges,
    flux_networks,
    foundations,
    immersive_engineering,
    industrial_foregoing,
    late_game,
    mekanism,
    mekanism_generators,
    modern_industrialization,
    powah,
    refined_storage,
    rftools,
    storage_gear,
)

_CHAPTER_MODULES = [
    foundations,
    create_factory,
    storage_gear,
    automation,
    refined_storage,
    powah,
    rftools,
    flux_networks,
    mekanism,
    mekanism_generators,
    extreme_reactors,
    modern_industrialization,
    industrial_foregoing,
    immersive_engineering,
    factory_challenges,
    late_game,
]


def all_chapters() -> list[Chapter]:
    return [mod.chapter() for mod in _CHAPTER_MODULES]
