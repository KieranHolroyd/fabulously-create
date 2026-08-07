"""15. Factory Challenges quest chapter."""
from __future__ import annotations

from ftb_quests.ast import Chapter, Quest, require, xp_levels
from ftb_quests.ids import (
    C_BRASS,
    C_PRECISION,
    FLUX_GARGANTUAN,
    MEKANISM_ATOMIC_ALLOY,
)
from ftb_quests.text import tutorial


def _challenge(
    n: int,
    x: float,
    y: float,
    task: str,
    count: int,
    title: str,
    goal: str,
    proof: str,
    *,
    link: int | None = None,
    deps: list[int] | None = None,
    size: float = 1.0,
    shape: str | None = None,
) -> Quest:
    return Quest(
        n=n,
        x=x,
        y=y,
        task=task,
        task_count=count,
        title=title,
        desc=tutorial(goal, why=proof),
        deps=deps or [],
        links=require(link) if link is not None else [],
        rewards=[xp_levels(3 if size > 1 else 2)],
        optional=True,
        hide_until_deps=True,
        size=size,
        shape=shape,
        subtitle="Factory challenge",
    )


def chapter() -> Chapter:
    quests = [
        _challenge(
            0, 0, 0, "create:andesite_alloy", 256, "Alloy on Tap",
            "Stockpile 256 andesite alloy.",
            "A stable Create workshop starts with alloy made faster than you spend it.",
            link=C_BRASS,
        ),
        _challenge(
            1, 0, 3, "create:brass_ingot", 128, "Brass Shift",
            "Produce 128 brass ingots.",
            "Continuous zinc, copper, heat, and mixing prove the brass line is dependable.",
            link=C_BRASS,
        ),
        _challenge(
            2, 3, 0, "refinedstorage:pattern", 32, "Pattern Library",
            "Encode 32 Refined Storage patterns.",
            "A pattern hall turns separate machines into one request-driven factory.",
        ),
        _challenge(
            3, 3, 3, "mekanism:alloy_atomic", 32, "Atomic Batch",
            "Produce 32 atomic alloys.",
            "The batch tests infusion materials, energy, and every alloy tier at once.",
            link=MEKANISM_ATOMIC_ALLOY,
        ),
        _challenge(
            4, 6, 0, "industrialforegoing:plastic", 64, "Polymer Line",
            "Produce 64 plastic.",
            "Latex extraction and processing should run as a loop, not a one-off craft.",
        ),
        _challenge(
            5, 6, 3, "modern_industrialization:electronic_circuit", 32, "Circuit Run",
            "Produce 32 electronic circuits.",
            "Repeatable circuits expose weak links across the electric machine chain.",
        ),
        _challenge(
            6, 9, 0, "immersiveengineering:ingot_steel", 64, "Industrial Steel",
            "Produce 64 Immersive Engineering steel ingots.",
            "A fed coke oven and blast furnace should deliver steel without babysitting.",
        ),
        _challenge(
            7, 9, 3, "bigreactors:ludicrite_ingot", 16, "Ludicrite Reserve",
            "Produce 16 ludicrite ingots.",
            "This reserve proves the reactor branch can sustain its most expensive material.",
        ),
        _challenge(
            8, 12, 0, "fluxnetworks:gargantuan_flux_storage", 1, "Grid Backbone",
            "Build gargantuan Flux storage.",
            "A serious factory needs wireless power buffering that survives demand spikes.",
            link=FLUX_GARGANTUAN,
        ),
        _challenge(
            9, 12, 3, "rftoolsdim:dimension_builder", 1, "Worldwright",
            "Build and power an RFTools Dimension Builder.",
            "Custom dimensions test sustained power, research, and remote logistics.",
        ),
        _challenge(
            10, 15, 1.5, "create:precision_mechanism", 256, "Factory Proven",
            "Deliver 256 precision mechanisms.",
            "The core material, alloy, and power tests feed this final proof of throughput.",
            link=C_PRECISION,
            deps=[0, 1, 3, 8],
            size=2.0,
            shape="gear",
        ),
    ]
    return Chapter(
        key="factory_challenges",
        base=1000,
        chapter_id="0200000000000010",
        icon="create:precision_mechanism",
        title="15. Factory Challenges",
        subtitle="Optional throughput tests for complete, connected factories",
        quests=quests,
    )
