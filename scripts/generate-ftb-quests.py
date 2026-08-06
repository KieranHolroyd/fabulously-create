#!/usr/bin/env python3
"""Generate the Fabulously Create FTB Quests book.

Design goals:
- Teach Create + pack mods instead of bare item checklists
- Flexible chapter exploration with optional side quests
- One exciting weighted reward roll per quest, plus any configured XP
- Multi-line quest text with tips and next-step hints

Quest definitions live as an AST under scripts/ftb_quests/.
"""
from __future__ import annotations

import re
import secrets
from pathlib import Path

from ftb_quests import build_book
from ftb_quests.compile import CompiledChapter, compile_book

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "pack" / "config" / "ftbquests" / "quests"

GROUP_MAIN = "0100000000000001"
FILE_ID = "0000000000000001"
REWARD_TABLE_ID = "7100000000000001"
REWARD_TABLE_ID_LONG = int(REWARD_TABLE_ID, 16)

# Shared weighted pool used by every quest. Counts are deliberately useful,
# while progression-skipping prizes have very low weights. Grouped roughly
# common -> jackpot; every modded id here is confirmed to exist in this pack
# (pulled from real quest task items).
COOL_REWARDS = [
    # --- Vanilla staples (common-ish) ---
    ("minecraft:diamond", 8, 12.0),
    ("minecraft:emerald_block", 2, 10.0),
    ("minecraft:experience_bottle", 16, 10.0),
    ("minecraft:iron_ingot", 16, 11.0),
    ("minecraft:copper_ingot", 24, 10.0),
    ("minecraft:coal", 32, 9.0),
    ("minecraft:ender_eye", 6, 8.0),
    ("minecraft:blaze_rod", 12, 8.0),
    ("minecraft:leather", 16, 8.0),
    # --- Vanilla uncommon ---
    ("minecraft:shulker_shell", 4, 7.0),
    ("minecraft:echo_shard", 4, 6.0),
    ("minecraft:dragon_breath", 6, 6.0),
    ("minecraft:nautilus_shell", 8, 6.0),
    ("minecraft:wither_skeleton_skull", 2, 5.0),
    ("minecraft:beacon", 1, 2.0),
    # --- Vanilla rare / jackpot ---
    ("minecraft:heart_of_the_sea", 1, 4.0),
    ("minecraft:trident", 1, 3.0),
    ("minecraft:netherite_scrap", 3, 3.0),
    ("minecraft:netherite_upgrade_smithing_template", 1, 2.5),
    ("minecraft:ominous_trial_key", 2, 2.5),
    ("minecraft:heavy_core", 1, 1.5),
    ("minecraft:enchanted_golden_apple", 1, 1.0),
    ("minecraft:netherite_ingot", 1, 1.0),
    ("minecraft:totem_of_undying", 1, 1.0),
    ("minecraft:dragon_egg", 1, 0.4),
    ("minecraft:nether_star", 1, 0.5),
    ("minecraft:elytra", 1, 0.25),
    # --- Create ---
    ("create:zinc_ingot", 16, 10.0),
    ("create:brass_ingot", 8, 9.0),
    ("create:andesite_alloy", 16, 9.0),
    ("create:electron_tube", 4, 6.0),
    ("create:precision_mechanism", 2, 7.0),
    ("create:blaze_cake", 4, 6.0),
    ("create:sturdy_sheet", 4, 4.0),
    ("create_sa:brass_jetpack_chestplate", 1, 0.6),
    ("create_jetpack:jetpack", 1, 0.5),
    # --- Mekanism ---
    ("mekanism:ingot_osmium", 16, 9.0),
    ("mekanism:ingot_steel", 12, 8.0),
    ("mekanism:alloy_infused", 8, 6.0),
    ("mekanism:alloy_atomic", 4, 3.0),
    ("mekanism:advanced_control_circuit", 4, 3.5),
    ("mekanism:atomic_disassembler", 1, 0.8),
    ("mekanismgenerators:hohlraum", 1, 0.5),
    # --- Powah ---
    ("powah:uraninite", 8, 5.0),
    ("powah:dielectric_paste", 8, 5.0),
    ("powah:steel_energized", 8, 5.0),
    ("powah:crystal_blazing", 2, 3.0),
    ("powah:crystal_niotic", 2, 2.0),
    ("powah:crystal_nitro", 1, 1.0),
    ("powah:crystal_spirited", 1, 0.8),
    # --- Immersive Engineering ---
    ("immersiveengineering:ingot_steel", 12, 8.0),
    ("immersiveengineering:coal_coke", 12, 7.0),
    ("immersiveengineering:hemp_fiber", 16, 6.0),
    ("immersiveengineering:graphite_electrode", 2, 3.0),
    # --- Modern Industrialization ---
    ("modern_industrialization:bronze_ingot", 12, 8.0),
    ("modern_industrialization:steel_ingot", 12, 7.0),
    ("modern_industrialization:electronic_circuit", 6, 5.0),
    ("modern_industrialization:digital_circuit", 3, 3.0),
    ("modern_industrialization:motor", 2, 3.0),
    # --- Industrial Foregoing ---
    ("industrialforegoing:pink_slime", 4, 3.0),
    ("industrialforegoing:plastic", 8, 5.0),
    ("industrialforegoing:machine_frame_advanced", 1, 1.5),
    # --- Refined Storage ---
    ("refinedstorage:quartz_enriched_iron", 8, 6.0),
    ("refinedstorage:16k_storage_disk", 1, 2.5),
    ("refinedstorage:wireless_grid", 1, 1.5),
    # --- RFTools ---
    ("rftoolsbase:dimensionalshard", 4, 4.0),
    ("rftoolspower:cell1", 1, 2.0),
    # --- Flux Networks ---
    ("fluxnetworks:flux_dust", 8, 5.0),
    ("fluxnetworks:basic_flux_storage", 1, 2.5),
    # --- Extreme Reactors (Big Reactors) ---
    ("bigreactors:yellorium_ingot", 8, 4.0),
    ("bigreactors:graphite_ingot", 8, 5.0),
    ("bigreactors:cyanite_ingot", 4, 3.0),
    ("bigreactors:ludicrite_ingot", 2, 1.0),
    # --- Silent Gear ---
    ("silentgear:blueprint_paper", 4, 5.0),
    ("silentgear:pickaxe_blueprint", 1, 2.0),
    ("silentgear:sword_blueprint", 1, 2.0),
    # --- Storage / QoL ---
    ("sophisticatedbackpacks:iron_backpack", 1, 3.0),
    ("sophisticatedbackpacks:stack_upgrade_tier_1", 1, 3.0),
    ("sophisticatedstorage:iron_chest", 1, 2.5),
    ("ironchest:diamond_chest", 1, 1.0),
    ("ironjetpacks:cell", 2, 2.0),
    ("waystones:warp_stone", 1, 5.0),
    ("naturescompass:naturescompass", 1, 2.0),
    ("tombstone:grave_dust", 4, 4.0),
]

# FTB Quests treats &X as a formatting code (0-9, a-f, k-o, r). Literal & must be \&.
_BARE_AMP = re.compile(r"(?<!\\)&(?![0-9a-fk-orA-FK-OR])")


def hid() -> str:
    """Random 16-hex-digit FTB Quests id.

    FTB Quests ids are parsed as signed 64-bit longs; a leading hex digit
    of 8-F overflows Long.MAX_VALUE and gets silently discarded/regenerated
    at load, orphaning any lang file keys that reference the original id.
    Keep the leading nibble in 0-7.
    """
    first = secrets.choice("01234567")
    rest = secrets.token_hex(8).upper()[1:]
    return first + rest


def escape_ftb_ampersands(s: str) -> str:
    """Escape literal & so FTB Quests doesn't treat it as a format code."""
    return _BARE_AMP.sub(r"\\&", s)


def snbt_escape(s: str) -> str:
    s = escape_ftb_ampersands(s)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    # FTB Quests reads each quest_desc entry as a single-line SNBT string;
    # a raw newline breaks the quoted string across lines and corrupts the
    # file. Line breaks must be the literal two-char escape `\n` instead.
    return s.replace("\n", "\\n")


def format_desc(desc: str | list[str]) -> list[str]:
    if isinstance(desc, str):
        return [desc]
    return list(desc)


def quest_snbt(
    qid: str,
    *,
    x: float,
    y: float,
    task_item: str,
    task_count: int = 1,
    rewards: list[dict] | None = None,
    deps: list[str] | None = None,
    optional: bool = False,
    size: float = 1.0,
    shape: str | None = None,
    hide_until_deps: bool = False,
) -> str:
    deps = deps or []
    configured_rewards = rewards or [{"type": "xp_levels", "xp_levels": 1}]
    # Item rewards are replaced by one shared random-table roll. XP remains a
    # guaranteed bonus where the quest definition explicitly included it.
    rewards = [{"type": "random"}] + [
        reward for reward in configured_rewards if reward["type"] in {"xp", "xp_levels"}
    ]
    lines = ["\t\t{"]
    if deps:
        if len(deps) == 1:
            lines.append(f'\t\t\tdependencies: ["{deps[0]}"]')
        else:
            lines.append("\t\t\tdependencies: [")
            for d in deps:
                lines.append(f'\t\t\t\t"{d}"')
            lines.append("\t\t\t]")
    if hide_until_deps and deps:
        lines.append("\t\t\thide_until_deps_visible: true")
    lines.append(f'\t\t\tid: "{qid}"')
    if optional:
        lines.append("\t\t\toptional: true")
    if shape:
        lines.append(f'\t\t\tshape: "{shape}"')
    if size != 1.0:
        lines.append(f"\t\t\tsize: {size:.1f}d")

    lines.append("\t\t\trewards: [")
    reward_blocks = []
    for r in rewards:
        rid = f"05{int(qid[2:], 16):014X}" if r["type"] == "random" else hid()
        rb = ["\t\t\t\t{"]
        rtype = r["type"]
        if rtype == "item":
            count = r.get("count", 1)
            rb.append(f'\t\t\t\t\tid: "{rid}"')
            rb.append("\t\t\t\t\titem: {")
            rb.append(f"\t\t\t\t\t\tcount: {count}")
            rb.append(f'\t\t\t\t\t\tid: "{r["item"]}"')
            rb.append("\t\t\t\t\t}")
            rb.append('\t\t\t\t\ttype: "item"')
        elif rtype == "xp":
            rb.append(f'\t\t\t\t\tid: "{rid}"')
            rb.append('\t\t\t\t\ttype: "xp"')
            rb.append(f'\t\t\t\t\txp: {r.get("xp", 50)}')
        elif rtype == "xp_levels":
            rb.append(f'\t\t\t\t\tid: "{rid}"')
            rb.append('\t\t\t\t\ttype: "xp"')
            rb.append(f'\t\t\t\t\txp_levels: {r.get("xp_levels", 1)}')
        elif rtype == "random":
            rb.append(f'\t\t\t\t\tid: "{rid}"')
            rb.append(f"\t\t\t\t\ttable_id: {REWARD_TABLE_ID_LONG}L")
            rb.append('\t\t\t\t\ttype: "random"')
        else:
            raise ValueError(f"unknown reward type {rtype}")
        rb.append("\t\t\t\t}")
        reward_blocks.append("\n".join(rb))
    lines.append(",\n".join(reward_blocks))
    lines.append("\t\t\t]")

    lines.append("\t\t\ttasks: [{")
    lines.append(f'\t\t\t\tid: "{hid()}"')
    lines.append(f'\t\t\t\titem: {{ count: {task_count}, id: "{task_item}" }}')
    lines.append('\t\t\t\ttype: "item"')
    lines.append("\t\t\t}]")
    lines.append(f"\t\t\tx: {x:.1f}d")
    lines.append(f"\t\t\ty: {y:.1f}d")
    lines.append("\t\t}")
    return "\n".join(lines)


def write_reward_table() -> None:
    """Write the shared weighted pool consumed by RandomReward."""
    lines = [
        "{",
        f'\tid: "{REWARD_TABLE_ID}"',
        "\tloot_size: 1",
        "\trewards: [",
    ]
    entries = []
    for index, (item_id, count, weight) in enumerate(COOL_REWARDS, start=1):
        reward_id = f"7200000000{index:06X}"
        entries.append(
            "\n".join(
                [
                    "\t\t{",
                    f'\t\t\tid: "{reward_id}"',
                    "\t\t\titem: {",
                    f"\t\t\t\tcount: {count}",
                    f'\t\t\t\tid: "{item_id}"',
                    "\t\t\t}",
                    f"\t\t\tweight: {weight:g}f",
                    "\t\t}",
                ]
            )
        )
    lines.append(",\n".join(entries))
    lines.extend(["\t]", '\ttitle: "Quest Treasure"', "}", ""])
    table_dir = QUESTS / "reward_tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    (table_dir / "quest_treasure.snbt").write_text("\n".join(lines), encoding="utf-8")


def quest_link_snbt(link: dict) -> str:
    lines = [
        "\t\t{",
        f'\t\t\tid: "{link["id"]}"',
        f'\t\t\tlinked_quest: "{link["linked_quest"]}"',
    ]
    if link.get("shape"):
        lines.append(f'\t\t\tshape: "{link["shape"]}"')
    size = link.get("size", 1.0)
    if size != 1.0:
        lines.append(f"\t\t\tsize: {size:.2f}d".replace(".00d", ".0d"))
    lines.append(f'\t\t\tx: {link["x"]:.1f}d')
    lines.append(f'\t\t\ty: {link["y"]:.1f}d')
    lines.append("\t\t}")
    return "\n".join(lines)


def quest_lang_lines(chapter: CompiledChapter) -> list[str]:
    """Flat `quest.<id>.<key>` lang lines for one chapter's quests.

    FTB Quests (2101.1.x) only loads `quests/lang/<locale>.snbt` as a single
    flat file (non-recursive `Files.list`); a `lang/en_us/chapters/*.snbt`
    tree is silently ignored. All chapters' lines must be merged into one
    file — see `main()`.
    """
    lines: list[str] = []
    for qid, meta in chapter.lang.items():
        if "title" in meta:
            lines.append(f'\tquest.{qid}.title: "{snbt_escape(meta["title"])}"')
        if "subtitle" in meta:
            lines.append(f'\tquest.{qid}.quest_subtitle: "{snbt_escape(meta["subtitle"])}"')
        if "desc" in meta:
            parts = format_desc(meta["desc"])
            lines.append(f"\tquest.{qid}.quest_desc: [")
            for i, p in enumerate(parts):
                comma = "," if i < len(parts) - 1 else ""
                lines.append(f'\t\t"{snbt_escape(p)}"{comma}')
            lines.append("\t]")
    return lines


def write_chapter(chapter: CompiledChapter, order_index: int) -> None:
    blocks = [
        quest_snbt(
            q["id"],
            x=q["x"],
            y=q["y"],
            task_item=q["task"],
            task_count=q.get("task_count", 1),
            rewards=q.get("rewards"),
            deps=q.get("deps"),
            optional=q.get("optional", False),
            size=q.get("size", 1.0),
            shape=q.get("shape"),
            hide_until_deps=q.get("hide_until_deps", False),
        )
        for q in chapter.quests
    ]

    if chapter.quest_links:
        links_block = ",\n".join(quest_link_snbt(link) for link in chapter.quest_links)
        quest_links_snbt = "\tquest_links: [\n" + links_block + "\n\t]"
    else:
        quest_links_snbt = "\tquest_links: [ ]"

    content = "\n".join(
        [
            "{",
            "\tdefault_hide_dependency_lines: false",
            '\tdefault_quest_shape: "rsquare"',
            f'\tfilename: "{chapter.key}"',
            f'\tgroup: "{GROUP_MAIN}"',
            "\ticon: {",
            f'\t\tid: "{chapter.icon}"',
            "\t}",
            f'\tid: "{chapter.chapter_id}"',
            f"\torder_index: {order_index}",
            quest_links_snbt,
            "\tquests: [",
            ",\n".join(blocks),
            "\t]",
            f'\ttitle: "{snbt_escape(chapter.title)}"',
            "}",
            "",
        ]
    )
    path = QUESTS / "chapters" / f"{chapter.key}.snbt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    book = build_book()
    compiled = compile_book(book)

    QUESTS.mkdir(parents=True, exist_ok=True)
    (QUESTS / "chapters").mkdir(exist_ok=True)
    write_reward_table()
    (QUESTS / "lang").mkdir(parents=True, exist_ok=True)

    (QUESTS / "data.snbt").write_text(
        "\n".join(
            [
                "{",
                '\tdefault_autoclaim_rewards: "disabled"',
                "\tdefault_consume_items: false",
                "\tdefault_quest_disable_jei: false",
                '\tdefault_quest_shape: "rsquare"',
                "\tdefault_reward_team: true",
                "\tdetection_delay: 20",
                "\tdisable_gui: false",
                "\tdrop_loot_crates: false",
                "\temergency_items_cooldown: 300",
                "\tgrid_scale: 0.5d",
                "\ticon: {",
                '\t\tid: "create:brass_hand"',
                "\t}",
                '\tlock_message: ""',
                "\tpause_game: false",
                '\tprogression_mode: "linear"',
                "\tshow_lock_icons: true",
                "\tversion: 13",
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (QUESTS / "chapter_groups.snbt").write_text(
        "\n".join(
            [
                "{",
                "\tchapter_groups: [",
                "\t\t{",
                f'\t\t\tid: "{GROUP_MAIN}"',
                "\t\t}",
                "\t]",
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # FTB Quests (2101.1.x) reads/writes exactly one flat file per locale —
    # `quests/lang/<locale>.snbt`. The mod itself only ever creates this
    # flat file (confirmed by editing quest text in-game and inspecting the
    # server's config/ftbquests/quests/lang/ output); a split lang/<locale>/
    # tree is never read.
    #
    # The real cause of missing text wasn't the lang file shape at all: FTB
    # Quests ids are parsed as signed 64-bit longs, and any id whose leading
    # hex nibble is 8-F overflows Long.MAX_VALUE. Out-of-range ids get
    # silently discarded and regenerated at load, which orphans every lang
    # key referencing the original id — titles/subtitles happened to still
    # render because chapter titles are literal fields, not lang lookups.
    # See hid() and ftb_quests/ids.py:quest_id() for the id-range fix.
    lang_lines = [
        "{",
        f'\tfile.{FILE_ID}.title: "Fabulously Create"',
        f'\tchapter_group.{GROUP_MAIN}.title: "Main Progression"',
    ]
    for chapter in compiled.values():
        lang_lines.append(f'\tchapter.{chapter.chapter_id}.title: "{snbt_escape(chapter.title)}"')
        lang_lines.append(
            f'\tchapter.{chapter.chapter_id}.chapter_subtitle: '
            f'["{snbt_escape(chapter.subtitle)}"]'
        )
    for chapter in compiled.values():
        lang_lines.extend(quest_lang_lines(chapter))
    lang_lines.extend(["}", ""])
    (QUESTS / "lang" / "en_us.snbt").write_text("\n".join(lang_lines), encoding="utf-8")

    for order_index, chapter in enumerate(compiled.values()):
        write_chapter(chapter, order_index)

    total = sum(len(chapter.quests) for chapter in compiled.values())
    print(f"Generated {total} quests across {len(compiled)} chapters → {QUESTS}")


if __name__ == "__main__":
    main()
