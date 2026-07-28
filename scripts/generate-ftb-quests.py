#!/usr/bin/env python3
"""Generate Fabulously Create FTB Quests book (early → late progression)."""
from __future__ import annotations

import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "pack" / "config" / "ftbquests" / "quests"


def hid() -> str:
    return secrets.token_hex(8).upper()


GROUP_MAIN = "A100000000000001"
FILE_ID = "0000000000000001"

CHAPTERS = {
    "foundations": ("A200000000000001", "minecraft:iron_pickaxe"),
    "create_factory": ("A200000000000002", "create:cogwheel"),
    "storage_gear": ("A200000000000003", "sophisticatedbackpacks:backpack"),
    "automation": ("A200000000000004", "integrateddynamics:cable"),
    "late_game": ("A200000000000005", "minecraft:netherite_ingot"),
}


def snbt_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def quest(
    qid: str,
    *,
    x: float,
    y: float,
    task_item: str,
    task_count: int = 1,
    reward_item: str | None = None,
    reward_count: int = 1,
    deps: list[str] | None = None,
    optional: bool = False,
    size: float = 1.0,
) -> tuple[str, dict]:
    """Return (snbt_block, lang_entries)."""
    task_id = hid()
    reward_id = hid()
    deps = deps or []
    lines = ["\t\t{"]
    if deps:
        if len(deps) == 1:
            lines.append(f'\t\t\tdependencies: ["{deps[0]}"]')
        else:
            lines.append("\t\t\tdependencies: [")
            for d in deps:
                lines.append(f'\t\t\t\t"{d}"')
            lines.append("\t\t\t]")
    lines.append(f'\t\t\tid: "{qid}"')
    if optional:
        lines.append("\t\t\toptional: true")
    if size != 1.0:
        lines.append(f"\t\t\tsize: {size:.1f}d")
    # reward
    if reward_item:
        lines.append("\t\t\trewards: [{")
        if reward_count != 1:
            lines.append(f"\t\t\t\tcount: {reward_count}")
        lines.append(f'\t\t\t\tid: "{reward_id}"')
        lines.append("\t\t\t\titem: {")
        lines.append("\t\t\t\t\tcount: 1")
        lines.append(f'\t\t\t\t\tid: "{reward_item}"')
        lines.append("\t\t\t\t}")
        lines.append('\t\t\t\ttype: "item"')
        lines.append("\t\t\t}]")
    else:
        lines.append("\t\t\trewards: [{")
        lines.append(f'\t\t\t\tid: "{reward_id}"')
        lines.append('\t\t\t\ttype: "xp"')
        lines.append("\t\t\t\txp: 25")
        lines.append("\t\t\t}]")
    # task
    lines.append("\t\t\ttasks: [{")
    lines.append(f'\t\t\t\tid: "{task_id}"')
    lines.append(f"\t\t\t\titem: {{ count: {task_count}, id: \"{task_item}\" }}")
    lines.append('\t\t\t\ttype: "item"')
    lines.append("\t\t\t}]")
    lines.append(f"\t\t\tx: {x:.1f}d")
    lines.append(f"\t\t\ty: {y:.1f}d")
    lines.append("\t\t}")
    return "\n".join(lines), {}


def write_chapter(
    filename: str,
    chapter_id: str,
    icon: str,
    quests_meta: list[dict],
    lang_quests: dict[str, dict[str, str]],
) -> None:
    blocks = []
    for q in quests_meta:
        block, _ = quest(
            q["id"],
            x=q["x"],
            y=q["y"],
            task_item=q["task"],
            task_count=q.get("task_count", 1),
            reward_item=q.get("reward"),
            reward_count=q.get("reward_count", 1),
            deps=q.get("deps"),
            optional=q.get("optional", False),
            size=q.get("size", 1.0),
        )
        blocks.append(block)

    content = "\n".join(
        [
            "{",
            "\tdefault_hide_dependency_lines: false",
            '\tdefault_quest_shape: "circle"',
            f'\tfilename: "{filename}"',
            f'\tgroup: "{GROUP_MAIN}"',
            "\ticon: {",
            f'\t\tid: "{icon}"',
            "\t}",
            f'\tid: "{chapter_id}"',
            f'\torder_index: {q_order(filename)}',
            "\tquest_links: [ ]",
            "\tquests: [",
            ",\n".join(blocks),
            "\t]",
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
        if "desc" in meta:
            desc = snbt_escape(meta["desc"])
            lang_lines.append(f'\tquest.{qid}.quest_desc: ["{desc}"]')
        if "subtitle" in meta:
            lang_lines.append(
                f'\tquest.{qid}.quest_subtitle: "{snbt_escape(meta["subtitle"])}"'
            )
    lang_lines.append("}")
    lang_lines.append("")
    lang_path.write_text("\n".join(lang_lines), encoding="utf-8")


def q_order(filename: str) -> int:
    return {
        "foundations": 0,
        "create_factory": 1,
        "storage_gear": 2,
        "automation": 3,
        "late_game": 4,
    }[filename]


def main() -> None:
    # Stable-ish IDs for dependencies across regenerations: use fixed prefixes.
    def Q(n: int) -> str:
        return f"B1{n:014X}"

    # ---- Chapter 1: Foundations (early) ----
    f = []
    fl = {}
    # linear spine + side branches
    defs = [
        (0, 0.0, 0.0, "minecraft:oak_log", 16, "minecraft:apple", 8, None, "Gather Wood", "Collect oak logs to get started.", "Early"),
        (1, 1.5, 0.0, "minecraft:crafting_table", 1, "minecraft:stick", 16, [0], "Crafting Table", "Your first workstation.", "Early"),
        (2, 3.0, 0.0, "minecraft:cobblestone", 32, "minecraft:torch", 16, [1], "Stone Age", "Mine a stack of cobble.", "Early"),
        (3, 4.5, 0.0, "minecraft:furnace", 1, "minecraft:coal", 16, [2], "Smelting", "Craft a furnace.", "Early"),
        (4, 6.0, 0.0, "minecraft:iron_ingot", 16, "minecraft:iron_nugget", 32, [3], "Iron Supply", "Smelt a small iron stockpile.", "Early"),
        (5, 7.5, 0.0, "minecraft:iron_pickaxe", 1, "minecraft:raw_iron", 8, [4], "Iron Pickaxe", "Upgrade your mining.", "Early"),
        (6, 9.0, 0.0, "minecraft:diamond", 3, "minecraft:experience_bottle", 4, [5], "Diamonds!", "Find your first diamonds.", "Early"),
        (7, 3.0, 1.5, "minecraft:bread", 16, "minecraft:wheat_seeds", 16, [2], "Stay Fed", "Bake bread for early food.", "Early", True),
        (8, 4.5, 1.5, "farmersdelight:stove", 1, "farmersdelight:cabbage_seeds", 4, [3], "Farmer's Stove", "Start Farmer's Delight cooking.", "Early"),
        (9, 6.0, 1.5, "comforts:sleeping_bag_red", 1, "minecraft:white_wool", 8, [4], "Sleeping Bag", "Sleep safely in the Nether later.", "Early"),
        (10, 7.5, 1.5, "ironchest:iron_chest", 1, "minecraft:chest", 4, [4], "Iron Chest", "More storage than a wooden chest.", "Early"),
        (11, 9.0, 1.5, "ironfurnaces:iron_furnace", 1, "minecraft:coal_block", 2, [4], "Iron Furnace", "Faster smelting.", "Early"),
        (12, 10.5, 0.0, "waystones:waystone", 1, "minecraft:ender_pearl", 4, [6], "Waystone", "Set your first teleport point.", "Early"),
    ]
    for row in defs:
        n, x, y, task, tc, reward, rc, deps_idx, title, desc, sub, *rest = row
        optional = rest[0] if rest else False
        qid = Q(100 + n)
        dep_ids = [Q(100 + i) for i in (deps_idx or [])]
        f.append(
            {
                "id": qid,
                "x": x,
                "y": y,
                "task": task,
                "task_count": tc,
                "reward": reward,
                "reward_count": rc,
                "deps": dep_ids,
                "optional": optional,
                "size": 1.5 if n == 0 else 1.0,
            }
        )
        fl[qid] = {"title": title, "desc": desc, "subtitle": sub}

    # ---- Chapter 2: Create Factory ----
    c = []
    cl = {}
    create_defs = [
        (0, 0.0, 0.0, "create:andesite_alloy", 16, "minecraft:andesite", 32, None, "Andesite Alloy", "The foundation of Create.", "Create"),
        (1, 1.5, 0.0, "create:shaft", 8, "create:andesite_alloy", 8, [0], "Shafts", "Transmit rotation.", "Create"),
        (2, 3.0, 0.0, "create:cogwheel", 8, "minecraft:oak_planks", 32, [1], "Cogwheels", "Gear up your factory.", "Create"),
        (3, 4.5, 0.0, "create:large_cogwheel", 4, "create:cogwheel", 8, [2], "Large Cogwheels", "Bigger ratios.", "Create"),
        (4, 6.0, 0.0, "create:water_wheel", 1, "create:shaft", 8, [1], "Water Wheel", "Free kinetic power.", "Create"),
        (5, 3.0, 1.5, "create:andesite_casing", 8, "create:andesite_alloy", 8, [0], "Andesite Casing", "Machine chassis.", "Create"),
        (6, 4.5, 1.5, "create:mechanical_press", 1, "minecraft:iron_block", 2, [5], "Mechanical Press", "Compact and press items.", "Create"),
        (7, 6.0, 1.5, "create:basin", 1, "create:andesite_alloy", 8, [5], "Basin", "Mixing and bulk processing.", "Create"),
        (8, 7.5, 1.5, "create:mechanical_mixer", 1, "create:whisk", 1, [7], "Mechanical Mixer", "Automate recipes in a basin.", "Create"),
        (9, 4.5, -1.5, "create:millstone", 1, "minecraft:wheat", 32, [5], "Millstone", "Mill grains and more.", "Create"),
        (10, 6.0, -1.5, "create:encased_fan", 1, "minecraft:propeller", 1, [5], "Encased Fan", "Blast, smoke, and wash.", "Create"),
        (11, 7.5, 0.0, "create:belt_connector", 8, "minecraft:dried_kelp", 16, [2], "Belts", "Move items around.", "Create"),
        (12, 9.0, 0.0, "create:depot", 4, "create:andesite_alloy", 8, [11], "Depots", "Hold items for processing.", "Create"),
        (13, 9.0, 1.5, "create:crushing_wheel", 2, "minecraft:iron_ingot", 16, [5], "Crushing Wheels", "Crush ores efficiently.", "Create"),
        (14, 10.5, 0.0, "create:blaze_burner", 1, "minecraft:blaze_rod", 4, [6], "Blaze Burner", "Superheat for brass.", "Create"),
        (15, 12.0, 0.0, "create:brass_ingot", 16, "create:copper_sheet", 8, [14], "Brass Age", "Alloy brass for advanced Create.", "Create"),
        (16, 13.5, 0.0, "create:brass_casing", 8, "create:brass_ingot", 8, [15], "Brass Casing", "Advanced machine frames.", "Create"),
        (17, 15.0, 0.0, "create:electron_tube", 4, "minecraft:redstone", 16, [16], "Electron Tubes", "Smart components.", "Create"),
        (18, 16.5, 0.0, "create:precision_mechanism", 4, "create:electron_tube", 4, [17], "Precision Mechanisms", "Midgame Create crafting core.", "Create"),
        (19, 15.0, 1.5, "create:deployer", 1, "create:brass_hand", 1, [16], "Deployer", "Automate right-clicks.", "Create"),
        (20, 16.5, 1.5, "create:mechanical_arm", 1, "create:precision_mechanism", 1, [18], "Mechanical Arm", "Move items between inventories.", "Create"),
        (21, 15.0, -1.5, "create:steam_engine", 1, "create:copper_sheet", 16, [15], "Steam Engine", "High stress power.", "Create"),
    ]
    for row in create_defs:
        n, x, y, task, tc, reward, rc, deps_idx, title, desc, sub = row
        qid = Q(200 + n)
        dep_ids = [Q(200 + i) for i in (deps_idx or [])]
        c.append(
            {
                "id": qid,
                "x": x,
                "y": y,
                "task": task,
                "task_count": tc,
                "reward": reward,
                "reward_count": rc,
                "deps": dep_ids,
                "size": 1.5 if n == 0 else 1.0,
            }
        )
        cl[qid] = {"title": title, "desc": desc, "subtitle": sub}

    # ---- Chapter 3: Storage & Gear ----
    s = []
    sl = {}
    storage_defs = [
        (0, 0.0, 0.0, "sophisticatedbackpacks:backpack", 1, "minecraft:leather", 16, None, "Backpack", "Carry more with Sophisticated Backpacks.", "Storage"),
        (1, 1.5, 0.0, "functionalstorage:oak_1", 2, "minecraft:chest", 4, [0], "Drawers", "Compact storage with Functional Storage.", "Storage"),
        (2, 3.0, 0.0, "toms_storage:inventory_connector", 1, "minecraft:ender_pearl", 2, [1], "Tom's Connector", "Begin networked storage.", "Storage"),
        (3, 4.5, 0.0, "pipez:item_pipe", 16, "minecraft:iron_ingot", 16, [1], "Item Pipes", "Move items with Pipez.", "Storage"),
        (4, 6.0, 0.0, "pipez:fluid_pipe", 8, "minecraft:copper_ingot", 16, [3], "Fluid Pipes", "Pipe fluids too.", "Storage"),
        (5, 1.5, 1.5, "silentgear:pickaxe_blueprint", 1, "silentgear:template_board", 4, [0], "Silent Blueprint", "Start modular Silent Gear tools.", "Gear"),
        (6, 3.0, 1.5, "silentgear:axe_blueprint", 1, "minecraft:oak_log", 32, [5], "Axe Blueprint", "Expand your Silent Gear set.", "Gear"),
        (7, 4.5, 1.5, "constructionstick:iron_stick", 1, "minecraft:iron_ingot", 16, [0], "Construction Stick", "Build faster.", "Building"),
        (8, 6.0, 1.5, "buildinggadgets2:gadget_building", 1, "minecraft:redstone", 32, [7], "Building Gadget", "Mass-build structures.", "Building"),
        (9, 7.5, 0.0, "ironchest:gold_chest", 1, "minecraft:gold_ingot", 16, [3], "Gold Chest", "Upgrade your chest tier.", "Storage"),
        (10, 7.5, 1.5, "ironfurnaces:gold_furnace", 1, "minecraft:gold_ingot", 16, [3], "Gold Furnace", "Even faster smelting.", "Storage"),
        (11, 9.0, 0.0, "artifacts:umbrella", 1, "minecraft:phantom_membrane", 4, [0], "Artifact Find", "Find an Artifacts trinket (umbrella).", "Gear", True),
    ]
    for row in storage_defs:
        n, x, y, task, tc, reward, rc, deps_idx, title, desc, sub, *rest = row
        optional = rest[0] if rest else False
        qid = Q(300 + n)
        dep_ids = [Q(300 + i) for i in (deps_idx or [])]
        s.append(
            {
                "id": qid,
                "x": x,
                "y": y,
                "task": task,
                "task_count": tc,
                "reward": reward,
                "reward_count": rc,
                "deps": dep_ids,
                "optional": optional,
                "size": 1.5 if n == 0 else 1.0,
            }
        )
        sl[qid] = {"title": title, "desc": desc, "subtitle": sub}

    # ---- Chapter 4: Automation ----
    a = []
    al = {}
    auto_defs = [
        (0, 0.0, 0.0, "integrateddynamics:cable", 16, "integrateddynamics:crystalized_menril_chunk", 8, None, "Logic Cable", "Start an Integrated Dynamics network.", "Automation"),
        (1, 1.5, 0.0, "integrateddynamics:variable", 8, "integrateddynamics:cable", 8, [0], "Variables", "Program your network.", "Automation"),
        (2, 3.0, 0.0, "integrateddynamics:part_inventory_reader", 1, "integrateddynamics:variable", 4, [1], "Inventory Reader", "Read inventories into logic.", "Automation"),
        (3, 4.5, 0.0, "integratedtunnels:part_interface_item", 2, "minecraft:hopper", 4, [0], "Item Interface", "Pull/push items with Tunnels.", "Automation"),
        (4, 6.0, 0.0, "integratedterminals:part_terminal_storage", 1, "minecraft:ender_eye", 2, [3], "Storage Terminal", "Browse networked storage.", "Automation"),
        (5, 3.0, 1.5, "createaddition:alternator", 1, "createaddition:capacitor", 2, [0], "Alternator", "Turn SU into FE.", "Power"),
        (6, 4.5, 1.5, "createaddition:electric_motor", 1, "createaddition:copper_spool", 4, [5], "Electric Motor", "Turn FE back into SU.", "Power"),
        (7, 6.0, 1.5, "createdieselgenerators:diesel_engine", 1, "createdieselgenerators:plant_oil_bucket", 2, [5], "Diesel Engine", "Burn diesel for power.", "Power"),
        (8, 7.5, 0.0, "create_enchantment_industry:blaze_enchanter", 1, "create_enchantment_industry:enchanting_template", 2, [4], "Blaze Enchanter", "Automate enchanting.", "Automation"),
        (9, 7.5, 1.5, "create_connected:brake", 1, "create:electron_tube", 2, [5], "Create Connected", "Use Connected utilities (Brake).", "Automation"),
        (10, 9.0, 0.0, "sliceanddice:slicer", 1, "farmersdelight:cutting_board", 1, [4], "Slice & Dice", "Automate Farmer's Delight cutting.", "Automation"),
        (11, 9.0, 1.5, "integratedcrafting:part_interface_crafting", 1, "minecraft:crafting_table", 1, [4], "Crafting Interface", "Autocraft on the ID network.", "Automation"),
    ]
    for row in auto_defs:
        n, x, y, task, tc, reward, rc, deps_idx, title, desc, sub = row
        qid = Q(400 + n)
        dep_ids = [Q(400 + i) for i in (deps_idx or [])]
        a.append(
            {
                "id": qid,
                "x": x,
                "y": y,
                "task": task,
                "task_count": tc,
                "reward": reward,
                "reward_count": rc,
                "deps": dep_ids,
                "size": 1.5 if n == 0 else 1.0,
            }
        )
        al[qid] = {"title": title, "desc": desc, "subtitle": sub}

    # ---- Chapter 5: Late Game ----
    l = []
    ll = {}
    late_defs = [
        (0, 0.0, 0.0, "minecraft:netherite_ingot", 1, "minecraft:ancient_debris", 4, None, "Netherite", "Enter the late game.", "Late"),
        (1, 1.5, 0.0, "ironfurnaces:netherite_furnace", 1, "minecraft:netherite_ingot", 1, [0], "Netherite Furnace", "Top-tier smelting speed.", "Late"),
        (2, 3.0, 0.0, "ironchest:obsidian_chest", 1, "minecraft:obsidian", 16, [0], "Obsidian Chest", "Blast-resistant storage.", "Late"),
        (3, 4.5, 0.0, "ironjetpacks:thruster", 2, "ironjetpacks:basic_coil", 2, [0], "Jetpack Parts", "Craft Iron Jetpacks components.", "Late"),
        (4, 6.0, 0.0, "create_jetpack:jetpack", 1, "create:copper_backtank", 1, [0], "Create Jetpack", "Backtank-powered flight.", "Late"),
        (5, 3.0, 1.5, "createbigcannons:cannon_end", 1, "minecraft:iron_block", 4, [0], "Big Cannons", "Build a cannon end piece.", "Late"),
        (6, 4.5, 1.5, "railways:conductor_whistle", 1, "create:precision_mechanism", 2, [0], "Steam 'n' Rails", "Train conductor tools.", "Late"),
        (7, 6.0, 1.5, "create_sa:brass_jetpack_chestplate", 1, "create:brass_ingot", 16, [4], "Brass Jetpack", "Stuff 'N Additions flight gear.", "Late"),
        (8, 7.5, 0.0, "create:precision_mechanism", 16, "create:brass_sheet", 32, [4], "Mechanism Stockpile", "Stockpile precision mechanisms.", "Late"),
        (9, 9.0, 0.0, "minecraft:nether_star", 1, "minecraft:diamond_block", 2, [8], "Wither Down", "Defeat the Wither.", "Late"),
        (10, 10.5, 0.0, "minecraft:elytra", 1, "minecraft:firework_rocket", 16, [9], "Elytra", "End-game mobility.", "Late"),
        (11, 9.0, 1.5, "constructionstick:netherite_stick", 1, "minecraft:netherite_ingot", 1, [0], "Netherite Stick", "Ultimate building stick.", "Late"),
        (12, 7.5, 1.5, "tombstone:grave_dust", 8, "minecraft:bone", 32, [0], "Tombstone Dust", "Engage Corail Tombstone crafting.", "Late", True),
    ]
    for row in late_defs:
        n, x, y, task, tc, reward, rc, deps_idx, title, desc, sub, *rest = row
        optional = rest[0] if rest else False
        qid = Q(500 + n)
        dep_ids = [Q(500 + i) for i in (deps_idx or [])]
        l.append(
            {
                "id": qid,
                "x": x,
                "y": y,
                "task": task,
                "task_count": tc,
                "reward": reward,
                "reward_count": rc,
                "deps": dep_ids,
                "optional": optional,
                "size": 1.75 if n == 0 else (1.5 if n == 10 else 1.0),
            }
        )
        ll[qid] = {"title": title, "desc": desc, "subtitle": sub}

    # Write roots
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
                '\tdefault_quest_shape: "circle"',
                "\tdefault_reward_team: false",
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
    (QUESTS / "lang" / "en_us" / "chapter.snbt").write_text(
        "\n".join(
            [
                "{",
                f'\tchapter.{CHAPTERS["foundations"][0]}.title: "1. Foundations"',
                f'\tchapter.{CHAPTERS["foundations"][0]}.chapter_subtitle: ["Early game basics"]',
                f'\tchapter.{CHAPTERS["create_factory"][0]}.title: "2. Create Factory"',
                f'\tchapter.{CHAPTERS["create_factory"][0]}.chapter_subtitle: ["Kinetic engineering"]',
                f'\tchapter.{CHAPTERS["storage_gear"][0]}.title: "3. Storage & Gear"',
                f'\tchapter.{CHAPTERS["storage_gear"][0]}.chapter_subtitle: ["Packing and tools"]',
                f'\tchapter.{CHAPTERS["automation"][0]}.title: "4. Automation & Power"',
                f'\tchapter.{CHAPTERS["automation"][0]}.chapter_subtitle: ["ID, pipes, and FE"]',
                f'\tchapter.{CHAPTERS["late_game"][0]}.title: "5. Late Game"',
                f'\tchapter.{CHAPTERS["late_game"][0]}.chapter_subtitle: ["Netherite and beyond"]',
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    write_chapter("foundations", *CHAPTERS["foundations"], f, fl)
    write_chapter("create_factory", *CHAPTERS["create_factory"], c, cl)
    write_chapter("storage_gear", *CHAPTERS["storage_gear"], s, sl)
    write_chapter("automation", *CHAPTERS["automation"], a, al)
    write_chapter("late_game", *CHAPTERS["late_game"], l, ll)

    total = len(f) + len(c) + len(s) + len(a) + len(l)
    print(f"Generated {total} quests across 5 chapters → {QUESTS}")


if __name__ == "__main__":
    main()
