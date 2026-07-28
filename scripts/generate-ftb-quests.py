#!/usr/bin/env python3
"""Generate the Fabulously Create FTB Quests book.

Design goals:
- Teach Create + pack mods instead of bare item checklists
- Flexible chapter exploration with optional side quests
- Meaningful rewards (useful gear, not leftover sticks)
- Multi-line quest text with tips and next-step hints
"""
from __future__ import annotations

import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "pack" / "config" / "ftbquests" / "quests"

GROUP_MAIN = "A100000000000001"
FILE_ID = "0000000000000001"

CHAPTERS = {
    # filename -> (id, icon, title, subtitle)
    "foundations": (
        "A200000000000001",
        "minecraft:iron_pickaxe",
        "1. Getting Started",
        "Survive, smelt iron, set a waystone",
    ),
    "create_factory": (
        "A200000000000002",
        "create:cogwheel",
        "2. Turning Gears",
        "Kinetics, brass, and ore drills",
    ),
    "storage_gear": (
        "A200000000000003",
        "sophisticatedbackpacks:backpack",
        "3. Bags & Blades",
        "Backpacks, pipes, Silent Gear",
    ),
    "automation": (
        "A200000000000004",
        "integrateddynamics:cable",
        "4. Wires & Wits",
        "Integrated Dynamics, diesel, enchanting",
    ),
    "late_game": (
        "A200000000000005",
        "minecraft:netherite_ingot",
        "5. Beyond Brass",
        "Netherite, flight, and the finale",
    ),
}


def hid() -> str:
    return secrets.token_hex(8).upper()


def snbt_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def Q(n: int) -> str:
    """Stable quest IDs across regenerations."""
    return f"B1{n:014X}"


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
    rewards = rewards or [{"type": "xp_levels", "xp_levels": 1}]
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
        rid = hid()
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


def write_chapter(
    filename: str,
    chapter_id: str,
    icon: str,
    title: str,
    quests_meta: list[dict],
    lang_quests: dict[str, dict],
) -> None:
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
        for q in quests_meta
    ]

    order = {
        "foundations": 0,
        "create_factory": 1,
        "storage_gear": 2,
        "automation": 3,
        "late_game": 4,
    }[filename]

    content = "\n".join(
        [
            "{",
            "\tdefault_hide_dependency_lines: false",
            '\tdefault_quest_shape: "rsquare"',
            f'\tfilename: "{filename}"',
            f'\tgroup: "{GROUP_MAIN}"',
            "\ticon: {",
            f'\t\tid: "{icon}"',
            "\t}",
            f'\tid: "{chapter_id}"',
            f"\torder_index: {order}",
            "\tquest_links: [ ]",
            "\tquests: [",
            ",\n".join(blocks),
            "\t]",
            # Embedded so the UI never falls back to the filename
            f'\ttitle: "{snbt_escape(title)}"',
            "}",
            "",
        ]
    )
    path = QUESTS / "chapters" / f"{filename}.snbt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    lang_path = QUESTS / "lang" / "en_us" / "chapters" / f"{filename}.snbt"
    lang_path.parent.mkdir(parents=True, exist_ok=True)
    lang_lines = ["{"]
    for qid, meta in lang_quests.items():
        if "title" in meta:
            lang_lines.append(f'\tquest.{qid}.title: "{snbt_escape(meta["title"])}"')
        if "subtitle" in meta:
            lang_lines.append(
                f'\tquest.{qid}.quest_subtitle: "{snbt_escape(meta["subtitle"])}"'
            )
        if "desc" in meta:
            parts = format_desc(meta["desc"])
            lang_lines.append(f"\tquest.{qid}.quest_desc: [")
            for i, p in enumerate(parts):
                comma = "," if i < len(parts) - 1 else ""
                lang_lines.append(f'\t\t"{snbt_escape(p)}"{comma}')
            lang_lines.append("\t]")
    lang_lines.append("}")
    lang_lines.append("")
    lang_path.write_text("\n".join(lang_lines), encoding="utf-8")


def add(
    bag: list[dict],
    lang: dict[str, dict],
    n: int,
    base: int,
    x: float,
    y: float,
    task: str,
    title: str,
    desc: str | list[str],
    *,
    task_count: int = 1,
    deps: list[int] | None = None,
    rewards: list[dict] | None = None,
    optional: bool = False,
    size: float = 1.0,
    shape: str | None = None,
    subtitle: str = "",
    hide_until_deps: bool = False,
) -> str:
    qid = Q(base + n)
    dep_ids = [Q(base + i) for i in (deps or [])]
    bag.append(
        {
            "id": qid,
            "x": x,
            "y": y,
            "task": task,
            "task_count": task_count,
            "rewards": rewards,
            "deps": dep_ids,
            "optional": optional,
            "size": size,
            "shape": shape,
            "hide_until_deps": hide_until_deps,
        }
    )
    lang[qid] = {"title": title, "desc": desc, "subtitle": subtitle}
    return qid


def item(item_id: str, count: int = 1) -> dict:
    return {"type": "item", "item": item_id, "count": count}


def xp_levels(n: int = 1) -> dict:
    return {"type": "xp_levels", "xp_levels": n}


def main() -> None:
    # ---- Chapter 1: Foundations ----
    f: list[dict] = []
    fl: dict[str, dict] = {}
    B = 100

    add(
        f,
        fl,
        0,
        B,
        0,
        0,
        "minecraft:book",
        "Welcome to Fabulously Create",
        [
            "This quest book is your guided tour of the pack — Create factories, smarter storage, Silent Gear, and late-game toys.",
            "",
            "&6How to use this book:&r",
            "• Quests complete when the items are in your inventory (they are &anot consumed&r).",
            "• Optional quests are dashed — skip them anytime.",
            "• Chapters are &aflexible&r. Start Create when you have iron; come back for side goals.",
            "",
            "Claim rewards from completed quests. Good luck, engineer!",
        ],
        rewards=[item("minecraft:bread", 16), item("minecraft:torch", 32), xp_levels(1)],
        size=2.0,
        shape="gear",
        subtitle="Start here",
    )
    add(
        f,
        fl,
        1,
        B,
        2,
        0,
        "minecraft:oak_log",
        "Timber!",
        [
            "Punch a tree and gather &616 oak logs&r. Any wood works for crafting, but oak keeps recipes simple.",
            "",
            "&7Tip:&r Large Ore Veins is installed — ores spawn in huge clusters later. Explore caves once you have iron.",
        ],
        task_count=16,
        deps=[0],
        rewards=[item("minecraft:apple", 8), item("minecraft:stick", 32)],
        subtitle="Gathering",
    )
    add(
        f,
        fl,
        2,
        B,
        4,
        0,
        "minecraft:crafting_table",
        "Workbench",
        [
            "Craft a crafting table. This is still your best friend — Create machines automate later, but early recipes start here.",
        ],
        deps=[1],
        rewards=[item("minecraft:chest", 2), xp_levels(1)],
        subtitle="Gathering",
    )
    add(
        f,
        fl,
        3,
        B,
        6,
        0,
        "minecraft:cobblestone",
        "Stone Age",
        [
            "Mine &632 cobblestone&r. You'll burn through stone for furnaces, generators, and Create casings.",
            "",
            "&7Tip:&r A stone pickaxe unlocks iron ore. Don't dig straight down.",
        ],
        task_count=32,
        deps=[2],
        rewards=[item("minecraft:torch", 32), item("minecraft:coal", 16)],
        subtitle="Gathering",
    )
    add(
        f,
        fl,
        4,
        B,
        8,
        0,
        "minecraft:furnace",
        "First Fire",
        [
            "Craft a furnace and start smelting. Coal or charcoal both work — charcoal from log furnaces is fine if coal is scarce.",
        ],
        deps=[3],
        rewards=[item("minecraft:coal", 32), xp_levels(1)],
        subtitle="Smelting",
    )
    add(
        f,
        fl,
        5,
        B,
        10,
        0,
        "minecraft:iron_ingot",
        "Iron Stockpile",
        [
            "Smelt &616 iron ingots&r. Iron is the gate into Create (andesite alloy), Pipez, chests, and furnaces.",
            "",
            "When you find a vein, FTB Ultimine (hold &6Grave / `&r by default) clears connected blocks fast.",
        ],
        task_count=16,
        deps=[4],
        rewards=[
            item("minecraft:iron_pickaxe", 1),
            item("minecraft:shield", 1),
            xp_levels(2),
        ],
        size=1.5,
        subtitle="Iron",
    )
    add(
        f,
        fl,
        6,
        B,
        12,
        0,
        "minecraft:iron_pickaxe",
        "Iron Tools",
        [
            "Craft an iron pickaxe. Diamonds and better Create ores wait below Y=16 — bring torches and food.",
        ],
        deps=[5],
        rewards=[item("minecraft:cooked_beef", 16), item("minecraft:lantern", 8)],
        subtitle="Iron",
    )
    add(
        f,
        fl,
        7,
        B,
        14,
        0,
        "minecraft:diamond",
        "Sparkly Rocks",
        [
            "Find &63 diamonds&r. Save them for a pickaxe or enchanting table — Create's midgame wants brass more than full diamond armor.",
        ],
        task_count=3,
        deps=[6],
        rewards=[item("minecraft:experience_bottle", 8), xp_levels(2)],
        size=1.5,
        subtitle="Diamonds",
    )
    add(
        f,
        fl,
        8,
        B,
        16,
        0,
        "waystones:waystone",
        "Set a Waystone",
        [
            "Craft and place a Waystone near your base. Warp back after every mining trip — deaths hurt less with a recall point.",
            "",
            "Scrolls of Warp Stone (from Waystones) make temporary links while exploring.",
        ],
        deps=[7],
        rewards=[item("waystones:warp_stone", 1), item("minecraft:ender_pearl", 4)],
        size=1.5,
        shape="hexagon",
        subtitle="Travel",
    )

    # Foundations side branch — food / QoL
    add(
        f,
        fl,
        9,
        B,
        6,
        2,
        "minecraft:bread",
        "Carb Loading",
        [
            "Bake &616 bread&r. Hunger kills more early bases than creepers.",
            "",
            "Optional, but your future factory shifts will thank you.",
        ],
        task_count=16,
        deps=[3],
        rewards=[item("minecraft:wheat_seeds", 32), item("minecraft:bone_meal", 16)],
        optional=True,
        subtitle="Food",
    )
    add(
        f,
        fl,
        10,
        B,
        8,
        2,
        "farmersdelight:stove",
        "Farmer's Kitchen",
        [
            "Craft a Farmer's Delight stove. Cooking meals gives better saturation than plain steaks.",
            "",
            "Later, Slice & Dice lets Create automate cutting boards — see Automation.",
        ],
        deps=[4],
        rewards=[
            item("farmersdelight:cabbage_seeds", 4),
            item("farmersdelight:tomato_seeds", 4),
            item("farmersdelight:onion", 4),
        ],
        subtitle="Food",
    )
    add(
        f,
        fl,
        11,
        B,
        10,
        2,
        "comforts:sleeping_bag_red",
        "Portable Bed",
        [
            "Craft a sleeping bag. Unlike beds, it &adoesn't set your respawn&r — perfect for Nether trips and caves.",
        ],
        deps=[5],
        rewards=[item("minecraft:white_wool", 16), xp_levels(1)],
        optional=True,
        subtitle="QoL",
    )
    add(
        f,
        fl,
        12,
        B,
        12,
        2,
        "ironchest:iron_chest",
        "Iron Chest",
        [
            "Upgrade to an Iron Chest. More slots than wood, and you can keep upgrading toward gold / diamond / obsidian.",
        ],
        deps=[5],
        rewards=[item("minecraft:chest", 4), item("minecraft:iron_ingot", 8)],
        subtitle="Storage",
    )
    add(
        f,
        fl,
        13,
        B,
        12,
        3.5,
        "ironfurnaces:iron_furnace",
        "Iron Furnace",
        [
            "Craft an Iron Furnace for faster smelting. Gold and diamond tiers come later when throughput matters.",
        ],
        deps=[5],
        rewards=[item("minecraft:coal_block", 2), xp_levels(1)],
        subtitle="Smelting",
    )
    add(
        f,
        fl,
        14,
        B,
        10,
        -2,
        "naturescompass:naturescompass",
        "Nature's Compass",
        [
            "Craft a Nature's Compass to hunt biomes for Create rubber trees, Farmer's Delight crops, or building vibes.",
        ],
        deps=[5],
        rewards=[item("minecraft:map", 1), xp_levels(1)],
        optional=True,
        subtitle="Exploration",
    )
    add(
        f,
        fl,
        15,
        B,
        12,
        -2,
        "explorerscompass:explorerscompass",
        "Explorer's Compass",
        [
            "Craft an Explorer's Compass to locate structures. Handy for villages, strongholds, and loot routes.",
        ],
        deps=[5],
        rewards=[item("minecraft:ender_pearl", 2), xp_levels(1)],
        optional=True,
        subtitle="Exploration",
    )

    # ---- Chapter 2: Create Factory ----
    c: list[dict] = []
    cl: dict[str, dict] = {}
    B = 200

    add(
        c,
        cl,
        0,
        B,
        0,
        0,
        "create:andesite_alloy",
        "Andesite Alloy",
        [
            "Craft &616 andesite alloy&r — Create's basic component.",
            "",
            "&6Recipe:&r Andesite + iron nuggets (crafting) or via mixing later.",
            "Everything kinetic starts here. Stockpile more than you think you need.",
        ],
        task_count=16,
        rewards=[item("minecraft:andesite", 64), item("minecraft:iron_nugget", 32), xp_levels(1)],
        size=2.0,
        shape="gear",
        subtitle="Create basics",
    )
    add(
        c,
        cl,
        1,
        B,
        2.5,
        0,
        "create:shaft",
        "Shafts",
        [
            "Craft &68 shafts&r. Shafts carry rotation in a straight line.",
            "",
            "Hold a shaft and look at another to place long runs. Use a wrench (Create) to reverse direction.",
        ],
        task_count=8,
        deps=[0],
        rewards=[item("create:andesite_alloy", 8)],
        subtitle="Kinetics",
    )
    add(
        c,
        cl,
        2,
        B,
        5,
        0,
        "create:cogwheel",
        "Cogwheels",
        [
            "Craft &68 cogwheels&r. Small cogs turn corners and change shaft axis.",
            "",
            "&7Tip:&r Encasing cogs with andesite casing stops them interlocking sideways.",
        ],
        task_count=8,
        deps=[1],
        rewards=[item("minecraft:oak_planks", 64)],
        subtitle="Kinetics",
    )
    add(
        c,
        cl,
        3,
        B,
        7.5,
        0,
        "create:large_cogwheel",
        "Large Cogwheels",
        [
            "Craft &64 large cogwheels&r for gear ratios. Pair large + small to speed up or slow down machines (stress changes too!).",
        ],
        task_count=4,
        deps=[2],
        rewards=[item("create:cogwheel", 8), xp_levels(1)],
        subtitle="Kinetics",
    )
    add(
        c,
        cl,
        4,
        B,
        5,
        -2.5,
        "create:water_wheel",
        "Water Power",
        [
            "Craft a water wheel. Flowing water against the blades generates free SU (stress units).",
            "",
            "Early game: one or two wheels power a whole andesite workshop. Later you'll want steam or electricity.",
        ],
        deps=[1],
        rewards=[item("create:shaft", 16), item("minecraft:water_bucket", 2)],
        size=1.5,
        subtitle="Power",
    )
    add(
        c,
        cl,
        5,
        B,
        5,
        2.5,
        "create:andesite_casing",
        "Andesite Casing",
        [
            "Craft &68 andesite casings&r (stripped logs + andesite alloy). Almost every andesite machine is built on casing.",
        ],
        task_count=8,
        deps=[0],
        rewards=[item("create:andesite_alloy", 16)],
        subtitle="Machines",
    )
    add(
        c,
        cl,
        6,
        B,
        7.5,
        2.5,
        "create:mechanical_press",
        "Mechanical Press",
        [
            "Build a Mechanical Press. Presses compact plates, compact cobble paths, and smash items on a depot below.",
            "",
            "Power it with a shaft on the side. Place a depot or basin underneath.",
        ],
        deps=[5],
        rewards=[item("minecraft:iron_block", 2), xp_levels(1)],
        subtitle="Machines",
    )
    add(
        c,
        cl,
        7,
        B,
        10,
        2.5,
        "create:basin",
        "Basin",
        [
            "Craft a Basin. Mixers, presses, and fans use basins for bulk crafting — dough, alloys, concrete, and more.",
        ],
        deps=[5],
        rewards=[item("create:andesite_alloy", 8)],
        subtitle="Machines",
    )
    add(
        c,
        cl,
        8,
        B,
        12.5,
        2.5,
        "create:mechanical_mixer",
        "Mechanical Mixer",
        [
            "Build a Mechanical Mixer above a basin. Spin it to mix recipes (andesite alloy in bulk, dough, brass later with heat).",
            "",
            "Add a spout or funnel to automate inputs once belts are online.",
        ],
        deps=[7],
        rewards=[item("create:whisk", 1), xp_levels(1)],
        size=1.5,
        subtitle="Machines",
    )
    add(
        c,
        cl,
        9,
        B,
        7.5,
        4.5,
        "create:millstone",
        "Millstone",
        [
            "Build a Millstone. Mill wheat into flour, crush concrete dyes, and process early bulk goods with low stress cost.",
        ],
        deps=[5],
        rewards=[item("minecraft:wheat", 32)],
        optional=True,
        subtitle="Machines",
    )
    add(
        c,
        cl,
        10,
        B,
        10,
        4.5,
        "create:encased_fan",
        "Encased Fan",
        [
            "Build an Encased Fan. Point it at a processing path:",
            "• Over fire / lava → &6smoking / blasting&r",
            "• Through water → &6washing&r (nuggets from gravel!)",
            "• Through lava carefully → &6haunting&r",
        ],
        deps=[5],
        rewards=[item("create:propeller", 2), xp_levels(1)],
        subtitle="Machines",
    )
    add(
        c,
        cl,
        11,
        B,
        10,
        0,
        "create:belt_connector",
        "Belts",
        [
            "Craft &68 belt connectors&r (dried kelp + dried kelp blocks). Belts move items between depots, basins, and inventories.",
            "",
            "Right-click two shafts with belt connectors to stretch a belt.",
        ],
        task_count=8,
        deps=[2],
        rewards=[item("minecraft:dried_kelp", 32)],
        subtitle="Logistics",
    )
    add(
        c,
        cl,
        12,
        B,
        12.5,
        0,
        "create:depot",
        "Depots",
        [
            "Craft &64 depots&r. Depots hold a single item stack for presses, deployers, and belt handoff — the workbench of kinetics.",
        ],
        task_count=4,
        deps=[11],
        rewards=[item("create:andesite_alloy", 8), xp_levels(1)],
        subtitle="Logistics",
    )
    add(
        c,
        cl,
        13,
        B,
        12.5,
        -2.5,
        "create:crushing_wheel",
        "Crushing Wheels",
        [
            "Craft &62 crushing wheels&r and place them as a pair. Crush ores for &amore output&r than a plain furnace — huge early power spike.",
            "",
            "Wash crushed ores with a fan + water for extra nuggets.",
        ],
        task_count=2,
        deps=[5],
        rewards=[item("minecraft:iron_ingot", 24), xp_levels(2)],
        size=1.5,
        subtitle="Ores",
    )
    add(
        c,
        cl,
        14,
        B,
        15,
        0,
        "create:blaze_burner",
        "Blaze Burner",
        [
            "Craft a Blaze Burner (empty burner + blaze). Feed it with blaze cakes or fuel to &6superheat&r for brass and other heated mixes.",
            "",
            "Hunt a Nether fortress, or trade with piglins for rods.",
        ],
        deps=[6],
        rewards=[item("minecraft:blaze_rod", 8), item("minecraft:nether_wart", 8)],
        size=1.5,
        subtitle="Brass gate",
    )
    add(
        c,
        cl,
        15,
        B,
        17.5,
        0,
        "create:brass_ingot",
        "Brass Age",
        [
            "Produce &616 brass ingots&r (copper + zinc with a heated mixer).",
            "",
            "Brass unlocks smart mechanisms, deployers, arms, and most midgame Create addons.",
        ],
        task_count=16,
        deps=[14],
        rewards=[
            item("create:zinc_ingot", 16),
            item("minecraft:copper_ingot", 32),
            item("create:brass_sheet", 8),
            xp_levels(2),
        ],
        size=1.75,
        shape="hexagon",
        subtitle="Brass",
    )
    add(
        c,
        cl,
        16,
        B,
        20,
        0,
        "create:brass_casing",
        "Brass Casing",
        [
            "Craft &68 brass casings&r. These frame deployers, mechanical arms, smart chutes, and precision machines.",
        ],
        task_count=8,
        deps=[15],
        rewards=[item("create:brass_ingot", 8)],
        subtitle="Brass",
    )
    add(
        c,
        cl,
        17,
        B,
        22.5,
        0,
        "create:electron_tube",
        "Electron Tubes",
        [
            "Craft &64 electron tubes&r (polished rose quartz + iron plates). They're the redstone-smart part inside precision builds.",
        ],
        task_count=4,
        deps=[16],
        rewards=[item("minecraft:redstone", 32), item("create:rose_quartz", 8)],
        subtitle="Brass",
    )
    add(
        c,
        cl,
        18,
        B,
        25,
        0,
        "create:precision_mechanism",
        "Precision Mechanisms",
        [
            "Assemble &64 precision mechanisms&r on a mechanical crafter / sequenced assembly line.",
            "",
            "These are the midgame Create currency — arms, consoles, and many addons want them. Automate early.",
        ],
        task_count=4,
        deps=[17],
        rewards=[item("create:electron_tube", 4), xp_levels(3)],
        size=1.75,
        shape="gear",
        subtitle="Midgame",
    )
    add(
        c,
        cl,
        19,
        B,
        22.5,
        2.5,
        "create:deployer",
        "Deployer",
        [
            "Build a Deployer. It auto-uses items — applying tools, placing blocks, assembling sequences, farming, and more.",
        ],
        deps=[16],
        rewards=[item("create:brass_hand", 1), xp_levels(1)],
        subtitle="Brass machines",
    )
    add(
        c,
        cl,
        20,
        B,
        25,
        2.5,
        "create:mechanical_arm",
        "Mechanical Arm",
        [
            "Build a Mechanical Arm. Program inputs/outputs to move items between inventories, basins, and casings without belts everywhere.",
        ],
        deps=[18],
        rewards=[item("create:precision_mechanism", 1), xp_levels(2)],
        size=1.5,
        subtitle="Brass machines",
    )
    add(
        c,
        cl,
        21,
        B,
        20,
        -2.5,
        "create:steam_engine",
        "Steam Engine",
        [
            "Build a Steam Engine for serious SU. Pair with a fluid tank of water and blaze burners — the jump from water wheels to factories.",
        ],
        deps=[15],
        rewards=[item("create:copper_sheet", 16), xp_levels(2)],
        optional=True,
        subtitle="Power",
    )
    add(
        c,
        cl,
        22,
        B,
        15,
        4.5,
        "createoreexcavation:vein_finder",
        "Ore Excavation Scanner",
        [
            "Craft a Vein Finder from Create Ore Excavation. Scan for infinite ore veins, then plant a drilling machine.",
            "",
            "Perfect once crushing wheels make processing cheap.",
        ],
        deps=[13],
        rewards=[item("createoreexcavation:drill", 1), xp_levels(1)],
        optional=True,
        subtitle="Ores",
    )
    add(
        c,
        cl,
        23,
        B,
        17.5,
        4.5,
        "createoreexcavation:drilling_machine",
        "Drilling Machine",
        [
            "Build a Drilling Machine on a found vein. Feed it SU and drills for passive ore — the pack's answer to strip-mining forever.",
        ],
        deps=[22],
        rewards=[item("create:andesite_alloy", 32), xp_levels(2)],
        optional=True,
        size=1.5,
        subtitle="Ores",
    )
    add(
        c,
        cl,
        24,
        B,
        22.5,
        -2.5,
        "create_new_age:generator_coil",
        "New Age Coil",
        [
            "Craft a Create: New Age generator coil. New Age adds magnets and electrical generation that pairs with Create kinetics.",
        ],
        deps=[15],
        rewards=[item("create_new_age:copper_wire", 8), xp_levels(1)],
        optional=True,
        subtitle="Power",
    )

    # ---- Chapter 3: Storage & Gear ----
    s: list[dict] = []
    sl: dict[str, dict] = {}
    B = 300

    add(
        s,
        sl,
        0,
        B,
        0,
        0,
        "sophisticatedbackpacks:backpack",
        "Backpack",
        [
            "Craft a Sophisticated Backpack. Upgrade it with stack upgrades, magnet, feeding, tool swap — your inventory becomes a workshop.",
            "",
            "Right-click to open. Craft upgrades and install them in the backpack GUI.",
        ],
        rewards=[item("minecraft:leather", 16), item("minecraft:string", 16), xp_levels(1)],
        size=2.0,
        shape="gear",
        subtitle="Carry more",
    )
    add(
        s,
        sl,
        1,
        B,
        2.5,
        0,
        "functionalstorage:oak_1",
        "Drawers",
        [
            "Craft &62 Functional Storage drawers&r. Drawers compact a huge count of one item — perfect for cobble, andesite alloy, and ingots.",
        ],
        task_count=2,
        deps=[0],
        rewards=[item("minecraft:chest", 8)],
        subtitle="Storage",
    )
    add(
        s,
        sl,
        2,
        B,
        5,
        0,
        "toms_storage:inventory_connector",
        "Tom's Storage Hub",
        [
            "Craft Tom's Inventory Connector. Link nearby inventories and open them from a crafting terminal — lightweight digital storage.",
        ],
        deps=[1],
        rewards=[item("minecraft:ender_pearl", 4), xp_levels(1)],
        size=1.5,
        subtitle="Storage",
    )
    add(
        s,
        sl,
        3,
        B,
        2.5,
        2.5,
        "pipez:item_pipe",
        "Item Pipes",
        [
            "Craft &616 Pipez item pipes&r. Configure filters with a wrench — simpler than Create belts for chest-to-chest logistics.",
        ],
        task_count=16,
        deps=[1],
        rewards=[item("minecraft:iron_ingot", 16)],
        subtitle="Pipes",
    )
    add(
        s,
        sl,
        4,
        B,
        5,
        2.5,
        "pipez:fluid_pipe",
        "Fluid Pipes",
        [
            "Craft &68 fluid pipes&r. Move water, lava, chocolate, diesel, and Create fluids between tanks and machines.",
        ],
        task_count=8,
        deps=[3],
        rewards=[item("minecraft:copper_ingot", 16), xp_levels(1)],
        subtitle="Pipes",
    )
    add(
        s,
        sl,
        5,
        B,
        7.5,
        0,
        "ironchest:gold_chest",
        "Gold Chest",
        [
            "Upgrade to a Gold Chest when drawer networks aren't enough for mixed junk storage.",
        ],
        deps=[3],
        rewards=[item("minecraft:gold_ingot", 16)],
        optional=True,
        subtitle="Storage",
    )
    add(
        s,
        sl,
        6,
        B,
        7.5,
        2.5,
        "ironfurnaces:gold_furnace",
        "Gold Furnace",
        [
            "Craft a Gold Furnace for a big smelting speed jump. Diamond / netherite tiers wait in Late Game.",
        ],
        deps=[3],
        rewards=[item("minecraft:gold_ingot", 16), item("minecraft:coal_block", 4)],
        optional=True,
        subtitle="Smelting",
    )
    add(
        s,
        sl,
        7,
        B,
        2.5,
        -2.5,
        "silentgear:pickaxe_blueprint",
        "Silent Gear Blueprint",
        [
            "Craft a Silent Gear pickaxe blueprint. Modular tools let you mix materials — head, rod, tip — for mining speed and durability.",
            "",
            "Use the blueprint in a crafting table / Silent Gear station with materials from the pack.",
        ],
        deps=[0],
        rewards=[item("silentgear:template_board", 4), xp_levels(1)],
        subtitle="Gear",
    )
    add(
        s,
        sl,
        8,
        B,
        5,
        -2.5,
        "silentgear:axe_blueprint",
        "Axe Blueprint",
        [
            "Expand Silent Gear with an axe blueprint. Matching material sets feel great once you have a favorite alloy.",
        ],
        deps=[7],
        rewards=[item("minecraft:oak_log", 64)],
        optional=True,
        subtitle="Gear",
    )
    add(
        s,
        sl,
        9,
        B,
        7.5,
        -2.5,
        "constructionstick:iron_stick",
        "Construction Stick",
        [
            "Craft an Iron Construction Stick. Extend walls and platforms in one click — faster base building before Building Gadgets.",
        ],
        deps=[0],
        rewards=[item("minecraft:iron_ingot", 16)],
        subtitle="Building",
    )
    add(
        s,
        sl,
        10,
        B,
        10,
        -2.5,
        "buildinggadgets2:gadget_building",
        "Building Gadget",
        [
            "Craft a Building Gadget 2. Copy / build / exchange blocks in bulk — perfect for factories and railways.",
        ],
        deps=[9],
        rewards=[item("minecraft:redstone", 32), xp_levels(2)],
        size=1.5,
        subtitle="Building",
    )
    add(
        s,
        sl,
        11,
        B,
        10,
        0,
        "artifacts:umbrella",
        "Artifact Hunt",
        [
            "Find an Artifacts umbrella (or any artifact). Trinkets drop from chests, mobs, and exploration — Curios slots equip them.",
            "",
            "Truly optional: treat it as a scavenger hunt.",
        ],
        deps=[0],
        rewards=[item("minecraft:phantom_membrane", 4), xp_levels(2)],
        optional=True,
        subtitle="Trinkets",
    )
    add(
        s,
        sl,
        12,
        B,
        10,
        2.5,
        "lootr:trophy",
        "Shared Loot Chests",
        [
            "Open a Lootr chest / barrel / shulker in a structure. Each player gets their own loot — no more racing your friends to the same chest.",
            "",
            "If this item is awkward to obtain, any lootr-tracked container completion still teaches the mod. Craft/find the trophy when available, or skip.",
        ],
        deps=[0],
        rewards=[item("minecraft:emerald", 8), xp_levels(1)],
        optional=True,
        subtitle="Exploration",
    )

    # Fix lootr trophy - may not exist. Check.
    # I'll verify and possibly use a different item.

    # ---- Chapter 4: Automation ----
    a: list[dict] = []
    al: dict[str, dict] = {}
    B = 400

    add(
        a,
        al,
        0,
        B,
        0,
        0,
        "integrateddynamics:cable",
        "Logic Network",
        [
            "Craft &616 Integrated Dynamics cables&r. ID is this pack's programmable logistics brain — readers, writers, and terminals plug into cable.",
            "",
            "Menril trees (deep dark / dark forests vibes depending on generation) supply menril for crafting.",
        ],
        task_count=16,
        rewards=[
            item("integrateddynamics:crystalized_menril_chunk", 16),
            xp_levels(1),
        ],
        size=2.0,
        shape="gear",
        subtitle="Integrated Dynamics",
    )
    add(
        a,
        al,
        1,
        B,
        2.5,
        0,
        "integrateddynamics:variable",
        "Variables",
        [
            "Craft &68 variables&r. Store numbers, items, lists, and logic — programming cards for your network.",
        ],
        task_count=8,
        deps=[0],
        rewards=[item("integrateddynamics:cable", 8)],
        subtitle="Integrated Dynamics",
    )
    add(
        a,
        al,
        2,
        B,
        5,
        0,
        "integrateddynamics:part_inventory_reader",
        "Inventory Reader",
        [
            "Craft an Inventory Reader part. Attach to a cable facing an inventory to read contents into variables.",
        ],
        deps=[1],
        rewards=[item("integrateddynamics:variable", 8), xp_levels(1)],
        subtitle="Integrated Dynamics",
    )
    add(
        a,
        al,
        3,
        B,
        2.5,
        2.5,
        "integratedtunnels:part_interface_item",
        "Item Tunnels",
        [
            "Craft &62 item interfaces&r (Integrated Tunnels). Pull and push items with filters — ID's version of import/export buses.",
        ],
        task_count=2,
        deps=[0],
        rewards=[item("minecraft:hopper", 4)],
        subtitle="Tunnels",
    )
    add(
        a,
        al,
        4,
        B,
        5,
        2.5,
        "integratedterminals:part_terminal_storage",
        "Storage Terminal",
        [
            "Craft a Storage Terminal. Browse and craft from everything your tunnels can see — the AE2 vibe without AE2.",
        ],
        deps=[3],
        rewards=[item("minecraft:ender_eye", 4), xp_levels(2)],
        size=1.5,
        shape="hexagon",
        subtitle="Tunnels",
    )
    add(
        a,
        al,
        5,
        B,
        7.5,
        2.5,
        "integratedcrafting:part_interface_crafting",
        "Crafting Interface",
        [
            "Craft a Crafting Interface. Request autocrafting through your ID terminal once patterns / recipes are set up.",
        ],
        deps=[4],
        rewards=[item("minecraft:crafting_table", 1), xp_levels(2)],
        size=1.5,
        subtitle="Tunnels",
    )
    add(
        a,
        al,
        6,
        B,
        2.5,
        -2.5,
        "createaddition:alternator",
        "Alternator",
        [
            "Build a Create Crafts & Additions Alternator. Spin it with SU to generate FE (Forge Energy) for electric addons.",
        ],
        deps=[0],
        rewards=[item("createaddition:capacitor", 2), xp_levels(1)],
        subtitle="Power",
    )
    add(
        a,
        al,
        7,
        B,
        5,
        -2.5,
        "createaddition:electric_motor",
        "Electric Motor",
        [
            "Build an Electric Motor to turn FE back into SU. Great for remote bases powered by diesel or New Age electricity.",
        ],
        deps=[6],
        rewards=[item("createaddition:copper_spool", 4), xp_levels(1)],
        subtitle="Power",
    )
    add(
        a,
        al,
        8,
        B,
        7.5,
        -2.5,
        "createdieselgenerators:diesel_engine",
        "Diesel Engine",
        [
            "Build a Diesel Engine. Process plant oil / crude into fuel and burn it for strong kinetic power — Create's combustion route.",
        ],
        deps=[6],
        rewards=[item("createdieselgenerators:plant_oil_bucket", 2), xp_levels(2)],
        size=1.5,
        subtitle="Power",
    )
    add(
        a,
        al,
        9,
        B,
        10,
        0,
        "create_enchantment_industry:blaze_enchanter",
        "Blaze Enchanter",
        [
            "Build a Blaze Enchanter from Enchantment Industry. Pump liquid experience and automate enchanted books / gear.",
        ],
        deps=[4],
        rewards=[
            item("create_enchantment_industry:enchanting_template", 2),
            xp_levels(2),
        ],
        size=1.5,
        subtitle="Magic factories",
    )
    add(
        a,
        al,
        10,
        B,
        10,
        2.5,
        "sliceanddice:slicer",
        "Slice & Dice",
        [
            "Craft a Slice & Dice slicer. Pair with Create to automate Farmer's Delight cutting — salads on a conveyor belt.",
        ],
        deps=[4],
        rewards=[item("farmersdelight:cutting_board", 1), xp_levels(1)],
        optional=True,
        subtitle="Food automation",
    )
    add(
        a,
        al,
        11,
        B,
        10,
        -2.5,
        "create_connected:brake",
        "Create: Connected",
        [
            "Craft a Brake from Create: Connected. Connected adds practical kinetic utilities — brakes, copycats-adjacent helpers, and more.",
        ],
        deps=[6],
        rewards=[item("create:electron_tube", 2), xp_levels(1)],
        optional=True,
        subtitle="Create extras",
    )

    # ---- Chapter 5: Late Game ----
    l: list[dict] = []
    ll: dict[str, dict] = {}
    B = 500

    add(
        l,
        ll,
        0,
        B,
        0,
        0,
        "minecraft:netherite_ingot",
        "Netherite",
        [
            "Smith a netherite ingot. Ancient debris + gold in a smithing setup — the late-game material gate for this book.",
            "",
            "Bring fire resistance. Bring a waystone. Bring dignity.",
        ],
        rewards=[item("minecraft:ancient_debris", 4), xp_levels(3)],
        size=2.0,
        shape="gear",
        subtitle="Endgame gate",
    )
    add(
        l,
        ll,
        1,
        B,
        2.5,
        0,
        "ironfurnaces:netherite_furnace",
        "Netherite Furnace",
        [
            "Craft a Netherite Furnace — top-tier smelting speed for when your ore drill finally wakes up.",
        ],
        deps=[0],
        rewards=[item("minecraft:netherite_ingot", 1), xp_levels(2)],
        subtitle="Smelting",
    )
    add(
        l,
        ll,
        2,
        B,
        2.5,
        2.5,
        "ironchest:obsidian_chest",
        "Obsidian Chest",
        [
            "Craft an Obsidian Chest. Blast-resistant storage for bases that… experiment with Big Cannons.",
        ],
        deps=[0],
        rewards=[item("minecraft:obsidian", 32)],
        optional=True,
        subtitle="Storage",
    )
    add(
        l,
        ll,
        3,
        B,
        5,
        0,
        "ironjetpacks:thruster",
        "Jetpack Thrusters",
        [
            "Craft &62 Iron Jetpacks thrusters&r. Combine with coils, capacitors, and a strap to assemble modular jetpacks.",
        ],
        task_count=2,
        deps=[0],
        rewards=[item("ironjetpacks:basic_coil", 2), xp_levels(1)],
        subtitle="Flight",
    )
    add(
        l,
        ll,
        4,
        B,
        7.5,
        0,
        "ironjetpacks:jetpack",
        "Iron Jetpack",
        [
            "Assemble an Iron Jetpacks jetpack. Charge it and take to the skies — independent from Create backtanks.",
        ],
        deps=[3],
        rewards=[xp_levels(3)],
        size=1.5,
        shape="hexagon",
        subtitle="Flight",
    )
    add(
        l,
        ll,
        5,
        B,
        5,
        -2.5,
        "create_jetpack:jetpack",
        "Create Jetpack",
        [
            "Craft the Create Jetpack. It runs off a copper backtank pressure — perfect if your factory already fills tanks.",
        ],
        deps=[0],
        rewards=[item("create:copper_backtank", 1), xp_levels(2)],
        size=1.5,
        subtitle="Flight",
    )
    add(
        l,
        ll,
        6,
        B,
        7.5,
        -2.5,
        "create_sa:brass_jetpack_chestplate",
        "Brass Jetpack",
        [
            "Craft Stuff 'N Additions brass jetpack chestplate — another flight option for brass-rich factories.",
        ],
        deps=[5],
        rewards=[item("create:brass_ingot", 16), xp_levels(2)],
        optional=True,
        subtitle="Flight",
    )
    add(
        l,
        ll,
        7,
        B,
        5,
        2.5,
        "createbigcannons:cannon_end",
        "Big Cannons",
        [
            "Craft a cannon end from Create Big Cannons. Build responsibly. Or don't. We put it in the pack either way.",
        ],
        deps=[0],
        rewards=[item("minecraft:iron_block", 4), xp_levels(1)],
        optional=True,
        subtitle="Chaos",
    )
    add(
        l,
        ll,
        8,
        B,
        7.5,
        2.5,
        "railways:conductor_whistle",
        "Steam 'n' Rails",
        [
            "Craft a conductor whistle. Trains, conductors, and fancy tracks — link factories across the map.",
        ],
        deps=[0],
        rewards=[item("create:precision_mechanism", 2), xp_levels(2)],
        optional=True,
        subtitle="Trains",
    )
    add(
        l,
        ll,
        9,
        B,
        10,
        0,
        "create:precision_mechanism",
        "Mechanism Stockpile",
        [
            "Stockpile &616 precision mechanisms&r. If this hurts, your assembly line isn't automated enough yet — go fix that.",
        ],
        task_count=16,
        deps=[4],
        rewards=[item("create:brass_sheet", 32), xp_levels(3)],
        size=1.5,
        subtitle="Logistics flex",
    )
    add(
        l,
        ll,
        10,
        B,
        12.5,
        0,
        "minecraft:nether_star",
        "Wither Down",
        [
            "Defeat the Wither and hold a nether star. Beacon bases make Create factories feel unfair in the best way.",
        ],
        deps=[9],
        rewards=[item("minecraft:diamond_block", 2), xp_levels(5)],
        size=1.75,
        shape="pentagon",
        subtitle="Boss",
    )
    add(
        l,
        ll,
        11,
        B,
        15,
        0,
        "minecraft:elytra",
        "Elytra",
        [
            "Claim elytra from the End. Combine with a jetpack or fireworks — you're done with walking.",
            "",
            "&6You've reached the end of the quest book.&r Keep building absurd factories.",
        ],
        deps=[10],
        rewards=[
            item("minecraft:firework_rocket", 64),
            item("minecraft:shulker_shell", 4),
            xp_levels(5),
        ],
        size=2.0,
        shape="gear",
        subtitle="Finale",
    )
    add(
        l,
        ll,
        12,
        B,
        10,
        2.5,
        "constructionstick:netherite_stick",
        "Netherite Construction Stick",
        [
            "Craft the netherite construction stick — maximum reach building for megabases.",
        ],
        deps=[0],
        rewards=[xp_levels(2)],
        optional=True,
        subtitle="Building",
    )
    add(
        l,
        ll,
        13,
        B,
        10,
        -2.5,
        "tombstone:grave_dust",
        "Tombstone Dust",
        [
            "Collect &68 grave dust&r from Corail Tombstone. Graves protect your items on death — dust feeds magic crafts.",
        ],
        task_count=8,
        deps=[0],
        rewards=[item("minecraft:bone", 32), xp_levels(1)],
        optional=True,
        subtitle="Death QoL",
    )

    # Replace lootr trophy quest if item missing — check and fix storage chapter quest 12
    # Use lootr:trophy only if exists; else use minecraft:filled_map as exploration proxy
    lootr_ok = False
    try:
        import zipfile
        from pathlib import Path as P

        mods = (
            P.home()
            / "Library/Application Support/PrismLauncher/instances/Fabulously Create/minecraft/mods"
        )
        for jar in mods.glob("lootr*.jar"):
            z = zipfile.ZipFile(jar)
            if any("trophy" in n for n in z.namelist()):
                lootr_ok = True
                break
    except Exception:
        pass
    if not lootr_ok:
        # rewrite quest 12 in storage to use chest / explorer vibe
        for q in s:
            if q["id"] == Q(300 + 12):
                q["task"] = "minecraft:ender_eye"
                q["task_count"] = 1
        sl[Q(300 + 12)] = {
            "title": "Structure Scout",
            "subtitle": "Exploration",
            "desc": [
                "Craft an Eye of Ender (or collect one). Use it toward stronghold energy — and remember Lootr makes structure chests per-player in this pack.",
                "",
                "Optional scavenger quest: celebrate by raiding any structure with friends without loot drama.",
            ],
        }

    # Write book metadata
    QUESTS.mkdir(parents=True, exist_ok=True)
    (QUESTS / "chapters").mkdir(exist_ok=True)
    (QUESTS / "lang" / "en_us" / "chapters").mkdir(parents=True, exist_ok=True)

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
                '\tprogression_mode: "flexible"',
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

    (QUESTS / "lang" / "en_us" / "file.snbt").write_text(
        "{\n"
        f'\tfile.{FILE_ID}.title: "Fabulously Create"\n'
        "}\n",
        encoding="utf-8",
    )
    (QUESTS / "lang" / "en_us" / "chapter_group.snbt").write_text(
        "{\n"
        f'\tchapter_group.{GROUP_MAIN}.title: "Main Progression"\n'
        "}\n",
        encoding="utf-8",
    )
    chapter_lang = ["{"]
    for _key, (cid, _icon, title, subtitle) in CHAPTERS.items():
        chapter_lang.append(f'\tchapter.{cid}.title: "{snbt_escape(title)}"')
        chapter_lang.append(
            f'\tchapter.{cid}.chapter_subtitle: ["{snbt_escape(subtitle)}"]'
        )
    chapter_lang.extend(["}", ""])
    (QUESTS / "lang" / "en_us" / "chapter.snbt").write_text(
        "\n".join(chapter_lang),
        encoding="utf-8",
    )

    write_chapter("foundations", *CHAPTERS["foundations"][:3], f, fl)
    write_chapter("create_factory", *CHAPTERS["create_factory"][:3], c, cl)
    write_chapter("storage_gear", *CHAPTERS["storage_gear"][:3], s, sl)
    write_chapter("automation", *CHAPTERS["automation"][:3], a, al)
    write_chapter("late_game", *CHAPTERS["late_game"][:3], l, ll)

    total = len(f) + len(c) + len(s) + len(a) + len(l)
    print(f"Generated {total} quests across 5 chapters → {QUESTS}")


if __name__ == "__main__":
    main()
