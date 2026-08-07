"""Book-wide quest curation: remove filler and loosen optional paths."""
from __future__ import annotations

from dataclasses import replace

from .ast import Book


# Absolute quest numbers deliberately retired from the book. These were
# terminal, optional shopping-list errands with no progression below them.
RETIRED_QUESTS = {
    105,  # spare coal after the furnace already teaches fuel
    313,  # gold chest duplicated three other storage upgrade lines
    314,  # gold furnace duplicated the main furnace progression
    423,  # niche gearbox with no follow-on lesson
    446,  # wrench errand between the RFTools frame and actual machines
    502,  # optional chest tiers made digital storage feel like a step back
    503,
    518,  # construction-stick tier repeat
    519,  # isolated grave-dust collection errand
}

# Optional leaf quests that should read as discoveries, not progression gates.
# They intentionally float without dependency lines in the quest map.
STANDALONE_QUESTS = {
    119,  # Nature's Compass
    120,  # Explorer's Compass
    122,  # Furnish the Base
    239,  # Copper Magnet
    323,  # Faucet
    422,  # Kinetic Brake
}


def polish_book(book: Book) -> Book:
    """Apply intentional removals and standalone side-quest rules."""
    found: set[int] = set()
    standalone_found: set[int] = set()
    chapters = []
    for chapter in book.chapters:
        quests = []
        for quest in chapter.quests:
            absolute = chapter.base + quest.n
            if absolute in RETIRED_QUESTS:
                found.add(absolute)
                continue
            if absolute in STANDALONE_QUESTS:
                if not quest.optional:
                    raise ValueError(f"standalone quest {absolute} must be optional")
                standalone_found.add(absolute)
                quests.append(replace(quest, deps=[], links=[]))
            else:
                quests.append(quest)
        chapters.append(replace(chapter, quests=quests))

    missing = RETIRED_QUESTS - found
    if missing:
        raise ValueError(f"retired quest ids no longer exist: {sorted(missing)}")
    missing_standalone = STANDALONE_QUESTS - standalone_found
    if missing_standalone:
        raise ValueError(
            f"standalone quest ids no longer exist: {sorted(missing_standalone)}"
        )
    return Book(chapters=chapters)
