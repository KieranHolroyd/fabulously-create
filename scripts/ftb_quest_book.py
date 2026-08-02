"""Quest definitions for Fabulously Create FTB Quests.

Each chapter builder returns (quests_meta, lang_map).
Descriptions use & formatting codes; literal & is escaped by the generator.

Absolute quest numbers (for cross-chapter `links=`):
  Foundations 100+, Create 200+, Storage 300+, Automation 400+, Late 500+.
"""
from __future__ import annotations

from typing import Callable

# Cross-chapter bridge targets (absolute = chapter_base + n)
F_IRON = 106
F_WAYSTONE = 110
F_LEATHER = 123
C_BRASS = 223
C_PRECISION = 227
C_TRACK = 238
S_BACKPACK = 300
S_TERMINAL = 309
A_TERMINAL = 409


def goal(
    what: str,
    *body: str,
    tip: str | None = None,
    nxt: str | None = None,
) -> list[str]:
    """Standard quest blurb: Goal → why → tip → next."""
    lines: list[str] = [f"&6Goal:&r {what}", ""]
    for para in body:
        lines.append(para)
        lines.append("")
    if tip:
        lines.append(f"&7Tip:&r {tip}")
    if nxt:
        lines.append(f"&7Next:&r {nxt}")
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def item(item_id: str, count: int = 1) -> dict:
    return {"type": "item", "item": item_id, "count": count}


def xp_levels(n: int = 1) -> dict:
    return {"type": "xp_levels", "xp_levels": n}


QuestAdder = Callable[..., str]


def chapter_foundations(add: QuestAdder) -> tuple[list[dict], dict[str, dict]]:
    f: list[dict] = []
    fl: dict[str, dict] = {}
    B = 100

    add(
        f, fl, 0, B, 0, 0, "minecraft:book",
        "Welcome to Fabulously Create",
        goal(
            "Open this book and claim your starter kit.",
            "This pack is about &6Create factories&r, smarter storage, Silent Gear tools, Integrated Dynamics logistics, and late-game flight.",
            "Quests complete when items are in your inventory — they are &anot consumed&r. Optional quests are dashed outlines; skip them anytime.",
            "Follow the &6dependency lines&r — chapters chain together (iron → Create → brass → automation → netherite). Side paths unlock as you progress.",
            tip="Claim rewards from completed quests. Use JEI (R) on any item you don't recognize.",
            nxt="Gather wood, stone, and iron — then plant a Waystone before you dig deep.",
        ),
        rewards=[item("minecraft:bread", 16), item("minecraft:torch", 32), xp_levels(1)],
        size=2.0, shape="gear", subtitle="Start here",
    )
    add(
        f, fl, 1, B, 2.5, 0, "minecraft:oak_log",
        "Timber!",
        goal(
            "Collect &616 oak logs&r.",
            "Wood is your first building block: crafting tables, charcoal, Create casings, and early chests all burn through logs.",
            tip="Any wood works for most recipes — explore once you have iron.",
            nxt="Craft a workbench, then start a stone stockpile.",
        ),
        task_count=16, deps=[0],
        rewards=[item("minecraft:apple", 8), item("minecraft:stick", 32)],
        subtitle="Gathering",
    )
    add(
        f, fl, 2, B, 5, 0, "minecraft:crafting_table",
        "Workbench",
        goal(
            "Craft a crafting table.",
            "Early recipes still start here. Create automates later — until then, a bench (or Crafting on a Stick) is your workshop.",
            nxt="Mine cobble for furnaces and generators.",
        ),
        deps=[1], rewards=[item("minecraft:chest", 2), xp_levels(1)], subtitle="Gathering",
    )
    add(
        f, fl, 3, B, 7.5, 0, "minecraft:cobblestone",
        "Stone Stockpile",
        goal(
            "Mine &664 cobblestone&r.",
            "Stone feeds furnaces, cobble gens, Create casings, and endless scaffolding. Grab more than feels polite.",
            tip="A stone pickaxe unlocks iron ore. Don't dig straight down.",
            nxt="Smelt a furnace, then hunt iron.",
        ),
        task_count=64, deps=[2],
        rewards=[item("minecraft:torch", 32), item("minecraft:coal", 16)],
        subtitle="Gathering",
    )
    add(
        f, fl, 4, B, 10, 0, "minecraft:furnace",
        "First Fire",
        goal(
            "Craft a furnace.",
            "Smelting unlocks metals. Coal is ideal; charcoal from logs works if caves are stingy.",
            nxt="Smelt a stack of iron — Create starts there.",
        ),
        deps=[3], rewards=[item("minecraft:coal", 32), xp_levels(1)], subtitle="Smelting",
    )
    add(
        f, fl, 5, B, 12.5, 0, "minecraft:coal",
        "Fuel Reserve",
        goal(
            "Stockpile &632 coal&r.",
            "Furnaces, Iron Furnaces, blaze burners (later), and long mining trips all want fuel on hand.",
            tip="Coal blocks compress storage. Charcoal works in furnaces too, but this quest wants coal ore/smelted coal.",
        ),
        task_count=32,
        deps=[4], hide_until_deps=True, rewards=[item("minecraft:coal_block", 2)],
        optional=True, subtitle="Fuel",
    )
    add(
        f, fl, 6, B, 12.5, -2, "minecraft:iron_ingot",
        "Iron Stockpile",
        goal(
            "Smelt &632 iron ingots&r.",
            "Iron is the pack's first real gate: Create andesite alloy, Pipez, Iron Chests/Furnaces, Construction Sticks, and more.",
            tip="FTB Ultimine (hold Grave / ` by default) clears connected ore fast when you hit a Large Ore Vein.",
            nxt="Make an iron pickaxe, then set a Waystone before deep caves.",
        ),
        task_count=32, deps=[4],
        rewards=[item("minecraft:iron_pickaxe", 1), item("minecraft:shield", 1), xp_levels(2)],
        size=1.5, subtitle="Iron",
    )
    add(
        f, fl, 7, B, 15, -2, "minecraft:iron_pickaxe",
        "Iron Tools",
        goal(
            "Craft an iron pickaxe.",
            "Diamonds and Create's deeper ores wait below. Bring food, torches, and a way home.",
            nxt="Find diamonds, then plant a Waystone at base.",
        ),
        deps=[6],
        rewards=[item("minecraft:cooked_beef", 16), item("minecraft:lantern", 8)],
        subtitle="Iron",
    )
    add(
        f, fl, 8, B, 15, 0, "minecraft:copper_ingot",
        "Copper Cache",
        goal(
            "Smelt &632 copper ingots&r.",
            "Copper becomes Create fluid pipes, backtanks, and brass (with zinc). Large copper veins are common — fill a chest.",
            tip="JEI: look ahead at brass and fluid tanks so you know why you're hoarding.",
        ),
        task_count=32,
        deps=[6], rewards=[item("minecraft:copper_block", 4), xp_levels(1)],
        subtitle="Metals",
    )
    add(
        f, fl, 9, B, 17.5, -2, "minecraft:diamond",
        "Sparkly Rocks",
        goal(
            "Find &65 diamonds&r.",
            "Save some for a pickaxe and enchanting. Create's midgame wants &6brass and precision mechanisms&r more than full diamond armor.",
            tip="Silent Gear can stretch materials further once you unlock blueprints.",
        ),
        task_count=5, deps=[7],
        rewards=[item("minecraft:experience_bottle", 8), xp_levels(2)],
        size=1.5, subtitle="Diamonds",
    )
    add(
        f, fl, 10, B, 20, -2, "waystones:waystone",
        "Set a Waystone",
        goal(
            "Craft and place a Waystone near your base.",
            "Warp home after every mining trip. Deaths hurt less with a recall point — especially once you hit the Nether for blaze burners.",
            tip="Warp Stones make temporary links while exploring. Sharestones help multiplayer bases.",
            nxt="You're ready for Turning Gears — or finish the food/QoL side path first.",
        ),
        deps=[9],
        rewards=[item("waystones:warp_stone", 1), item("minecraft:ender_pearl", 4)],
        size=1.5, shape="hexagon", subtitle="Travel",
    )
    add(
        f, fl, 11, B, 7.5, 2.5, "minecraft:bread",
        "Carb Loading",
        goal(
            "Bake &616 bread&r.",
            "Hunger kills more early bases than creepers. Keep a stack for every cave run.",
        ),
        task_count=16,
        deps=[3], hide_until_deps=True, rewards=[item("minecraft:wheat_seeds", 32), item("minecraft:bone_meal", 16)],
        optional=True, subtitle="Food",
    )
    add(
        f, fl, 12, B, 10, 2.5, "farmersdelight:cooking_pot",
        "Cooking Pot",
        goal(
            "Craft a Farmer's Delight cooking pot.",
            "Meals beat plain steaks for saturation. Pair with a cutting board and stove for a proper kitchen.",
            tip="Later, Slice & Dice lets Create automate cutting boards — see Wires & Wits.",
            nxt="Add a stove and knife when you're settled.",
        ),
        deps=[4], rewards=[
            item("farmersdelight:cabbage_seeds", 4),
            item("farmersdelight:tomato_seeds", 4),
            item("farmersdelight:onion", 4),
        ],
        subtitle="Food",
    )
    add(
        f, fl, 13, B, 12.5, 2.5, "farmersdelight:stove",
        "Farmer's Kitchen",
        goal(
            "Craft a Farmer's Delight stove.",
            "The stove is the heart of meal cooking — fire it up next to your cooking pot.",
        ),
        deps=[12], rewards=[item("farmersdelight:skillet", 1), xp_levels(1)],
        subtitle="Food",
    )
    add(
        f, fl, 14, B, 15, 2.5, "farmersdelight:iron_knife",
        "Kitchen Knife",
        goal(
            "Craft an iron knife.",
            "Knives process meats and plants on a cutting board — required for many Delight recipes.",
        ),
        deps=[13], hide_until_deps=True, rewards=[item("farmersdelight:cutting_board", 1)],
        optional=True, subtitle="Food",
    )
    add(
        f, fl, 15, B, 10, 4.5, "comforts:sleeping_bag_red",
        "Portable Bed",
        goal(
            "Craft a sleeping bag.",
            "Unlike beds, it &adoesn't set your respawn&r — perfect for Nether trips and caves without wrecking your Waystone home.",
        ),
        deps=[7], hide_until_deps=True, rewards=[item("minecraft:white_wool", 16), xp_levels(1)],
        optional=True, subtitle="QoL",
    )
    add(
        f, fl, 16, B, 12.5, 4.5, "crafting_on_a_stick:crafting_table",
        "Crafting on a Stick",
        goal(
            "Craft a crafting table on a stick.",
            "Portable crafting from your hotbar — huge quality-of-life while strip-mining or wiring factories.",
            tip="There are sticks for smithing, stonecutter, grindstone, and more.",
        ),
        deps=[7], rewards=[item("minecraft:stick", 16), xp_levels(1)],
        subtitle="QoL",
    )
    add(
        f, fl, 17, B, 15, 4.5, "ironchest:iron_chest",
        "Iron Chest",
        goal(
            "Upgrade to an Iron Chest.",
            "More slots than wood. Keep upgrading toward gold / diamond / obsidian as junk piles grow.",
            nxt="Iron Furnaces speed smelting while you prep Create.",
        ),
        deps=[6], rewards=[item("minecraft:chest", 4), item("minecraft:iron_ingot", 8)],
        subtitle="Storage",
    )
    add(
        f, fl, 18, B, 17.5, 4.5, "ironfurnaces:iron_furnace",
        "Iron Furnace",
        goal(
            "Craft an Iron Furnace.",
            "Faster smelting now; gold and diamond tiers wait until throughput really matters.",
        ),
        deps=[17], rewards=[item("minecraft:coal_block", 2), xp_levels(1)],
        subtitle="Smelting",
    )
    add(
        f, fl, 19, B, 10, -4, "naturescompass:naturescompass",
        "Nature's Compass",
        goal(
            "Craft a Nature's Compass.",
            "Hunt biomes for crops, building vibes, or menril-friendly areas before Integrated Dynamics.",
        ),
        deps=[10], hide_until_deps=True, rewards=[item("minecraft:map", 1), xp_levels(1)],
        optional=True, subtitle="Exploration",
    )
    add(
        f, fl, 20, B, 12.5, -4, "explorerscompass:explorerscompass",
        "Explorer's Compass",
        goal(
            "Craft an Explorer's Compass.",
            "Locate structures for loot. Reminder: &6Lootr&r makes structure chests per-player — no racing friends.",
        ),
        deps=[10], hide_until_deps=True, rewards=[item("minecraft:ender_pearl", 2), xp_levels(1)],
        optional=True, subtitle="Exploration",
    )
    add(
        f, fl, 21, B, 15, -4, "supplementaries:wrench",
        "Supplementaries Wrench",
        goal(
            "Craft a Supplementaries wrench.",
            "Rotate and tweak functional décor — faucets, turn tables, and more. Great alongside Create's own wrench.",
        ),
        deps=[16], hide_until_deps=True, rewards=[item("supplementaries:jar", 4)],
        optional=True, subtitle="Building",
    )
    add(
        f, fl, 22, B, 17.5, -4, "another_furniture:oak_chair",
        "Furnish the Base",
        goal(
            "Craft an oak chair (Another Furniture).",
            "Optional décor goal — make the base feel lived-in before the factory takes over every block.",
        ),
        deps=[17], hide_until_deps=True, rewards=[item("another_furniture:oak_table", 1), xp_levels(1)],
        optional=True, subtitle="Building",
    )
    add(
        f, fl, 23, B, 20, 0, "minecraft:leather",
        "Leather Bundle",
        goal(
            "Collect &616 leather&r.",
            "Backpacks, books, and early armor all want leather. Breed cows or hunt while exploring.",
            nxt="Bags & Blades opens with a Sophisticated Backpack.",
        ),
        task_count=16,
        deps=[6], hide_until_deps=True, rewards=[item("minecraft:string", 16), xp_levels(1)],
        optional=True, subtitle="Gathering",
    )

    return f, fl


def chapter_create(add: QuestAdder) -> tuple[list[dict], dict[str, dict]]:
    c: list[dict] = []
    cl: dict[str, dict] = {}
    B = 200

    add(
        c, cl, 0, B, 0, 0, "create:andesite_alloy",
        "Andesite Alloy",
        goal(
            "Craft &632 andesite alloy&r.",
            "Create's basic component. Everything kinetic — shafts, cogs, casings, presses — starts here.",
            tip="Recipe: andesite + iron nuggets in crafting, or bulk-mix later with a mixer + basin.",
            nxt="Hand-crank a few machines, then build water wheels for free SU.",
        ),
        task_count=32,
        links=[F_IRON], rewards=[item("minecraft:andesite", 64), item("minecraft:iron_nugget", 64), xp_levels(1)],
        size=2.0, shape="gear", subtitle="Create basics",
    )
    add(
        c, cl, 1, B, 2.5, 0, "create:hand_crank",
        "Hand Crank",
        goal(
            "Craft a hand crank.",
            "Manually spin early machines before water wheels. Great for testing a press or millstone setup.",
        ), deps=[0], rewards=[item("create:andesite_alloy", 8)], subtitle="Kinetics",
    )
    add(
        c, cl, 2, B, 5, 0, "create:shaft",
        "Shafts",
        goal(
            "Craft &616 shafts&r.",
            "Shafts carry rotation in a straight line. Hold a shaft and look at another to place long runs.",
            tip="Use a Create wrench to reverse rotation direction.",
        ),
        task_count=16,
        deps=[1], rewards=[item("create:andesite_alloy", 8)], subtitle="Kinetics",
    )
    add(
        c, cl, 3, B, 7.5, 0, "create:cogwheel",
        "Cogwheels",
        goal(
            "Craft &616 cogwheels&r.",
            "Small cogs turn corners and change shaft axis — the elbows of your kinetic network.",
            tip="Encasing cogs with andesite casing stops sideways interlocking.",
        ),
        task_count=16,
        deps=[2], rewards=[item("minecraft:oak_planks", 64)], subtitle="Kinetics",
    )
    add(
        c, cl, 4, B, 10, 0, "create:large_cogwheel",
        "Large Cogwheels",
        goal(
            "Craft &68 large cogwheels&r.",
            "Pair large + small for gear ratios — speed up or slow down machines (stress changes too).",
        ),
        task_count=8,
        deps=[3], rewards=[item("create:cogwheel", 8), xp_levels(1)], subtitle="Kinetics",
    )
    add(
        c, cl, 5, B, 5, -2.5, "create:water_wheel",
        "Water Power",
        goal(
            "Craft a water wheel.",
            "Flowing water against the blades generates free SU (stress units). One or two wheels power a whole andesite workshop.",
            tip="Later you'll want steam engines, diesel, or electricity for megabases.",
            nxt="Build andesite casings into a press + mixer line.",
        ),
        deps=[2], rewards=[item("create:shaft", 16), item("minecraft:water_bucket", 2)],
        size=1.5, subtitle="Power",
    )
    add(
        c, cl, 6, B, 5, -4.5, "create:windmill_bearing",
        "Windmill Bearing",
        goal(
            "Craft a windmill bearing.",
            "Sail-powered SU when you have space for a big windmill — optional alternative to water wheels.",
        ),
        deps=[5], hide_until_deps=True, rewards=[item("minecraft:white_wool", 32), xp_levels(1)],
        optional=True, subtitle="Power",
    )
    add(
        c, cl, 7, B, 5, 2.5, "create:andesite_casing",
        "Andesite Casing",
        goal(
            "Craft &616 andesite casings&r.",
            "Stripped logs + andesite alloy. Almost every andesite machine is built on casing.",
        ),
        task_count=16,
        deps=[2], rewards=[item("create:andesite_alloy", 16)], subtitle="Machines",
    )
    add(
        c, cl, 8, B, 7.5, 2.5, "create:mechanical_press",
        "Mechanical Press",
        goal(
            "Build a Mechanical Press.",
            "Presses compact plates, smash items on a depot, and unlock sheet metal for pipes and casings.",
            tip="Power from the side; put a depot or basin underneath.",
        ),
        deps=[7], rewards=[item("minecraft:iron_block", 2), xp_levels(1)], subtitle="Machines",
    )
    add(
        c, cl, 9, B, 10, 2.5, "create:basin",
        "Basin",
        goal(
            "Craft a Basin.",
            "Mixers, presses, and bulk crafting use basins — dough, alloys, concrete, brass later with heat.",
        ), deps=[7], rewards=[item("create:andesite_alloy", 8)], subtitle="Machines",
    )
    add(
        c, cl, 10, B, 12.5, 2.5, "create:mechanical_mixer",
        "Mechanical Mixer",
        goal(
            "Build a Mechanical Mixer above a basin.",
            "Bulk-craft andesite alloy, dough, and (with a blaze burner) brass. Automate inputs with funnels once belts exist.",
        ),
        deps=[9], rewards=[item("create:whisk", 1), xp_levels(1)],
        size=1.5, subtitle="Machines",
    )
    add(
        c, cl, 11, B, 7.5, 4.5, "create:millstone",
        "Millstone",
        goal(
            "Build a Millstone.",
            "Mill wheat into flour and process early bulk goods with low stress cost.",
        ),
        deps=[7], hide_until_deps=True, rewards=[item("minecraft:wheat", 32)],
        optional=True, subtitle="Machines",
    )
    add(
        c, cl, 12, B, 10, 4.5, "create:mechanical_saw",
        "Mechanical Saw",
        goal(
            "Build a Mechanical Saw.",
            "Auto-cut logs into planks and process wood at factory scale — huge for casing spam.",
        ),
        deps=[7], rewards=[item("minecraft:oak_log", 32), xp_levels(1)],
        subtitle="Machines",
    )
    add(
        c, cl, 13, B, 12.5, 4.5, "create:encased_fan",
        "Encased Fan",
        goal(
            "Build an Encased Fan.",
            "Point it at a processing path:",
            "• Over fire / lava → &6smoking / blasting&r",
            "• Through water → &6washing&r (nuggets from gravel!)",
            "• Through lava carefully → &6haunting&r",
            tip="Washing crushed ores after crushing wheels is a massive early ore multiplier.",
        ),
        deps=[7], rewards=[item("create:propeller", 2), xp_levels(1)],
        subtitle="Machines",
    )
    add(
        c, cl, 14, B, 10, -2.5, "create:belt_connector",
        "Belts",
        goal(
            "Craft &616 belt connectors&r.",
            "Belts move items between depots, basins, and inventories. Right-click two shafts to stretch a belt.",
            tip="Dried kelp farms pay for themselves once belts go wide.",
        ),
        task_count=16,
        deps=[3], rewards=[item("minecraft:dried_kelp", 32)], subtitle="Logistics",
    )
    add(
        c, cl, 15, B, 12.5, -2.5, "create:depot",
        "Depots",
        goal(
            "Craft &68 depots&r.",
            "Depots hold a single stack for presses, deployers, and belt handoff — the workbench of kinetics.",
        ),
        task_count=8,
        deps=[14], rewards=[item("create:andesite_alloy", 8), xp_levels(1)], subtitle="Logistics",
    )
    add(
        c, cl, 16, B, 15, -2.5, "create:andesite_funnel",
        "Andesite Funnels",
        goal(
            "Craft &68 andesite funnels&r.",
            "Pull and push items onto belts and into inventories. Brass funnels come later with filters.",
        ),
        task_count=8,
        deps=[15], rewards=[item("create:andesite_alloy", 8)], subtitle="Logistics",
    )
    add(
        c, cl, 17, B, 15, 0, "create:crushing_wheel",
        "Crushing Wheels",
        goal(
            "Craft &62 crushing wheels&r and place them as a pair.",
            "Crush ores for &amore output&r than a furnace — the pack's first real ore multiplier.",
            tip="Wash crushed ores with a fan + water for extra nuggets.",
            nxt="Hunt zinc, then blaze burners for brass.",
        ),
        task_count=2,
        deps=[8, 13], rewards=[item("minecraft:iron_ingot", 24), xp_levels(2)],
        size=1.5, subtitle="Ores",
    )
    add(
        c, cl, 18, B, 17.5, 0, "create:zinc_ingot",
        "Zinc Stockpile",
        goal(
            "Produce &616 zinc ingots&r.",
            "Zinc + copper (+ heat) = brass. Mine zinc ore or crush raw zinc.",
        ),
        task_count=16,
        deps=[17], rewards=[item("minecraft:copper_ingot", 32), xp_levels(1)],
        subtitle="Metals",
    )
    add(
        c, cl, 19, B, 17.5, 2.5, "create:fluid_tank",
        "Fluid Tanks",
        goal(
            "Craft &64 fluid tanks&r.",
            "Store water, lava, chocolate, plant oil, diesel, and liquid XP later. Stack tanks into towers.",
            nxt="Mechanical pumps and hose pulleys move fluids around the factory.",
        ),
        task_count=4,
        deps=[8], rewards=[item("minecraft:copper_ingot", 16)], subtitle="Fluids",
    )
    add(
        c, cl, 20, B, 20, 2.5, "create:mechanical_pump",
        "Mechanical Pump",
        goal(
            "Build a Mechanical Pump.",
            "Move fluids through Create pipes under SU power — water for steam, oil for diesel, XP for enchanting.",
        ),
        deps=[19], rewards=[item("create:copper_sheet", 8), xp_levels(1)], subtitle="Fluids",
    )
    add(
        c, cl, 21, B, 20, 4.5, "create:hose_pulley",
        "Hose Pulley",
        goal(
            "Craft a hose pulley.",
            "Drain or fill lakes and infinite fluid sources into your tank network.",
        ),
        deps=[20], hide_until_deps=True, rewards=[item("minecraft:dried_kelp", 16)],
        optional=True, subtitle="Fluids",
    )
    add(
        c, cl, 22, B, 20, 0, "create:blaze_burner",
        "Blaze Burner",
        goal(
            "Craft a Blaze Burner.",
            "Empty burner + blaze. Feed blaze cakes or fuel to &6superheat&r for brass and heated mixes.",
            tip="Nether fortress or piglin trades. Place a Waystone before the trip.",
            nxt="Mix copper + zinc with heat → brass age.",
        ),
        deps=[10], rewards=[item("minecraft:blaze_rod", 8), item("minecraft:nether_wart", 8)],
        size=1.5, subtitle="Brass gate",
    )
    add(
        c, cl, 23, B, 22.5, 0, "create:brass_ingot",
        "Brass Age",
        goal(
            "Produce &632 brass ingots&r.",
            "Brass unlocks smart mechanisms, deployers, arms, trains, and most midgame Create addons.",
            tip="Automate brass early — precision mechanisms will eat it forever.",
        ),
        task_count=32,
        deps=[18, 22], rewards=[
            item("create:zinc_ingot", 16),
            item("minecraft:copper_ingot", 32),
            item("create:brass_sheet", 16),
            xp_levels(2),
        ],
        size=1.75, shape="hexagon", subtitle="Brass",
    )
    add(
        c, cl, 24, B, 25, 0, "create:brass_casing",
        "Brass Casing",
        goal(
            "Craft &616 brass casings&r.",
            "Frames deployers, mechanical arms, smart chutes, and precision machines.",
        ),
        task_count=16,
        deps=[23], rewards=[item("create:brass_ingot", 8)], subtitle="Brass",
    )
    add(
        c, cl, 25, B, 27.5, 0, "create:electron_tube",
        "Electron Tubes",
        goal(
            "Craft &68 electron tubes&r.",
            "Polished rose quartz + iron plates. The redstone-smart part inside precision builds.",
        ),
        task_count=8,
        deps=[24], rewards=[item("minecraft:redstone", 32), item("create:rose_quartz", 8)],
        subtitle="Brass",
    )
    add(
        c, cl, 26, B, 30, 0, "create:mechanical_crafter",
        "Mechanical Crafters",
        goal(
            "Craft &69 mechanical crafters&r.",
            "Arrange them into a crafting grid for sequenced assembly — how precision mechanisms are born.",
            tip="JEI shows the assembly sequence. Automate inputs with funnels/arms.",
        ),
        task_count=9,
        deps=[25], rewards=[item("create:electron_tube", 4), xp_levels(2)],
        size=1.5, subtitle="Midgame",
    )
    add(
        c, cl, 27, B, 32.5, 0, "create:precision_mechanism",
        "Precision Mechanisms",
        goal(
            "Assemble &68 precision mechanisms&r.",
            "Midgame Create currency — arms, consoles, trains, and many addons want them.",
            tip="If crafting these by hand hurts, your factory isn't finished yet.",
            nxt="Deployers and arms next — then Ore Excavation for infinite ore.",
        ),
        task_count=8,
        deps=[26], rewards=[item("create:brass_sheet", 16), xp_levels(3)],
        size=1.75, shape="gear", subtitle="Midgame",
    )
    add(
        c, cl, 28, B, 27.5, 2.5, "create:deployer",
        "Deployer",
        goal(
            "Build a Deployer.",
            "Auto-uses items: applying tools, placing blocks, assembly sequences, farming, and more.",
        ),
        deps=[24], rewards=[item("create:brass_hand", 1), xp_levels(1)], subtitle="Brass machines",
    )
    add(
        c, cl, 29, B, 30, 2.5, "create:mechanical_arm",
        "Mechanical Arm",
        goal(
            "Build a Mechanical Arm.",
            "Program inputs/outputs to move items between inventories without belts everywhere.",
        ),
        deps=[27, 28], rewards=[item("create:precision_mechanism", 1), xp_levels(2)],
        size=1.5, subtitle="Brass machines",
    )
    add(
        c, cl, 30, B, 25, -2.5, "create:steam_engine",
        "Steam Engine",
        goal(
            "Build a Steam Engine.",
            "Serious SU from water tanks + blaze burners — the jump from water wheels to real factories.",
        ),
        deps=[23], hide_until_deps=True, rewards=[item("create:copper_sheet", 16), xp_levels(2)],
        optional=True, subtitle="Power",
    )
    add(
        c, cl, 31, B, 22.5, 4.5, "createoreexcavation:vein_finder",
        "Vein Finder",
        goal(
            "Craft a Vein Finder (Create Ore Excavation).",
            "Scan for infinite ore veins, then plant a drilling machine. The pack's answer to strip-mining forever.",
            tip="Best once crushing wheels make processing cheap.",
        ),
        deps=[17], rewards=[item("createoreexcavation:drill", 1), xp_levels(1)],
        subtitle="Ores",
    )
    add(
        c, cl, 32, B, 25, 4.5, "createoreexcavation:drilling_machine",
        "Drilling Machine",
        goal(
            "Build a Drilling Machine on a found vein.",
            "Feed it SU and drills for passive ore. Pair with crushing + washing for absurd ingot/hour.",
        ),
        deps=[31], rewards=[item("create:andesite_alloy", 32), xp_levels(2)],
        size=1.5, subtitle="Ores",
    )
    add(
        c, cl, 33, B, 27.5, -2.5, "create_new_age:generator_coil",
        "New Age Coil",
        goal(
            "Craft a Create: New Age generator coil.",
            "Magnets and electrical generation that pair with Create kinetics — another power path beside diesel and CCA.",
        ),
        deps=[23], hide_until_deps=True, rewards=[item("create_new_age:copper_wire", 8), xp_levels(1)],
        optional=True, subtitle="Power",
    )
    add(
        c, cl, 34, B, 30, -2.5, "create_new_age:basic_motor",
        "New Age Motor",
        goal(
            "Craft a basic motor (Create: New Age).",
            "Turn electrical power back into rotation for remote workshops.",
        ),
        deps=[33], hide_until_deps=True, rewards=[item("create_new_age:magnetite_block", 2), xp_levels(1)],
        optional=True, subtitle="Power",
    )
    add(
        c, cl, 35, B, 15, 6.5, "createdeco:andesite_catwalk",
        "Factory Catwalks",
        goal(
            "Craft an andesite catwalk (Create Deco).",
            "Industrial décor that makes factories readable — walkways, hulls, lamps, and sheet metal.",
        ),
        deps=[7], hide_until_deps=True, rewards=[item("createdeco:andesite_support", 8)],
        optional=True, subtitle="Building",
    )
    add(
        c, cl, 36, B, 17.5, 6.5, "copycats:copycat_block",
        "Copycat Block",
        goal(
            "Craft a Copycats+ copycat block.",
            "Disguise technical blocks as any material — hide cables and machines inside pretty walls.",
        ),
        deps=[35], hide_until_deps=True, rewards=[item("copycats:copycat_slab", 8), xp_levels(1)],
        optional=True, subtitle="Building",
    )
    add(
        c, cl, 37, B, 20, 6.5, "interiors:seatwood_planks",
        "Train Interiors",
        goal(
            "Craft seatwood planks (Create: Interiors).",
            "Furniture and seating for trains and stations — optional flair once tracks exist.",
        ),
        deps=[38], hide_until_deps=True, rewards=[item("interiors:white_chair", 2)],
        optional=True, subtitle="Building",
    )
    add(
        c, cl, 38, B, 32.5, 2.5, "create:track",
        "Train Track",
        goal(
            "Craft &616 Create train tracks&r.",
            "Trains move bulk items and players across the map. Steam 'n' Rails adds more track styles and conductors later.",
            nxt="Beyond Brass covers conductor whistles and fuel tanks.",
        ),
        task_count=16,
        deps=[27], rewards=[item("create:precision_mechanism", 1), xp_levels(1)],
        subtitle="Trains",
    )
    add(
        c, cl, 39, B, 22.5, -4.5, "create_sa:copper_magnet",
        "Copper Magnet",
        goal(
            "Craft a copper magnet (Stuff 'N Additions).",
            "Pull nearby items — great while mining or standing near crushing outputs.",
        ),
        deps=[28], hide_until_deps=True, rewards=[item("minecraft:iron_ingot", 16)],
        optional=True, subtitle="Tools",
    )

    return c, cl


def chapter_storage(add: QuestAdder) -> tuple[list[dict], dict[str, dict]]:
    s: list[dict] = []
    sl: dict[str, dict] = {}
    B = 300

    add(
        s, sl, 0, B, 0, 0, "sophisticatedbackpacks:backpack",
        "Backpack",
        goal(
            "Craft a Sophisticated Backpack.",
            "Upgrade it with stack, magnet, feeding, and tool-swap upgrades — your inventory becomes a workshop.",
            tip="Right-click to open. Craft upgrades and install them in the backpack GUI.",
            nxt="Iron backpack + stack upgrade, then drawers for bulk materials.",
        ),
        links=[F_IRON], rewards=[item("minecraft:leather", 16), item("minecraft:string", 16), xp_levels(1)],
        size=2.0, shape="gear", subtitle="Carry more",
    )
    add(
        s, sl, 1, B, 2.5, 0, "sophisticatedbackpacks:iron_backpack",
        "Iron Backpack",
        goal(
            "Upgrade to an Iron Backpack.",
            "More slots for long cave runs and factory wiring sessions.",
        ),
        deps=[0], rewards=[item("minecraft:iron_ingot", 16), xp_levels(1)],
        subtitle="Carry more",
    )
    add(
        s, sl, 2, B, 5, 0, "sophisticatedbackpacks:stack_upgrade_tier_1",
        "Stack Upgrade",
        goal(
            "Craft a stack upgrade (tier 1) for your backpack.",
            "Carry fewer slot types and more of what matters — alloy, sheets, mechanisms.",
        ),
        deps=[1], rewards=[item("sophisticatedbackpacks:pickup_upgrade", 1), xp_levels(1)],
        subtitle="Carry more",
    )
    add(
        s, sl, 3, B, 2.5, 2.5, "functionalstorage:oak_1",
        "Drawers",
        goal(
            "Craft &64 Functional Storage drawers&r.",
            "Drawers compact a huge count of one item — perfect for cobble, andesite alloy, and ingots.",
            nxt="Add a storage controller to talk to many drawers at once.",
        ),
        task_count=4,
        deps=[1], rewards=[item("minecraft:chest", 8)], subtitle="Storage",
    )
    add(
        s, sl, 4, B, 5, 2.5, "functionalstorage:storage_controller",
        "Drawer Controller",
        goal(
            "Craft a Functional Storage controller.",
            "Access a whole drawer wall from one block — pipe into the controller, not every drawer.",
        ),
        deps=[3], rewards=[item("minecraft:redstone", 16), xp_levels(1)],
        size=1.5, subtitle="Storage",
    )
    add(
        s, sl, 5, B, 7.5, 2.5, "functionalstorage:compacting_drawer",
        "Compacting Drawer",
        goal(
            "Craft a compacting drawer.",
            "Auto-crafts nuggets ↔ ingots ↔ blocks. Perfect for iron, gold, and Create metals.",
        ),
        deps=[4], hide_until_deps=True, rewards=[item("minecraft:iron_ingot", 32)],
        optional=True, subtitle="Storage",
    )
    add(
        s, sl, 6, B, 5, -2.5, "sophisticatedstorage:iron_chest",
        "Sophisticated Chest",
        goal(
            "Craft a Sophisticated Storage iron chest.",
            "Upgradeable chests/barrels with the same upgrade ecosystem as backpacks — filters, compacting, and more.",
        ),
        deps=[1], rewards=[item("minecraft:chest", 4), xp_levels(1)],
        subtitle="Storage",
    )
    add(
        s, sl, 7, B, 7.5, -2.5, "sophisticatedstorage:controller",
        "Storage Controller",
        goal(
            "Craft a Sophisticated Storage controller.",
            "Network nearby sophisticated containers for combined access.",
        ),
        deps=[6], hide_until_deps=True, rewards=[item("minecraft:ender_pearl", 2), xp_levels(1)],
        optional=True, subtitle="Storage",
    )
    add(
        s, sl, 8, B, 10, 0, "toms_storage:inventory_connector",
        "Tom's Storage Hub",
        goal(
            "Craft Tom's Inventory Connector.",
            "Link nearby inventories and browse them from a terminal — lightweight digital storage without AE2.",
            tip="Keep linked chests close; use cables for larger bases.",
            nxt="Add a crafting terminal for JEI-friendly crafting from the network.",
        ),
        deps=[4], rewards=[item("minecraft:ender_pearl", 4), xp_levels(1)],
        size=1.5, subtitle="Storage",
    )
    add(
        s, sl, 9, B, 12.5, 0, "toms_storage:crafting_terminal",
        "Crafting Terminal",
        goal(
            "Craft Tom's Crafting Terminal.",
            "Craft using everything the Inventory Connector can see. Pair with Pipez or Create for restocking.",
        ),
        deps=[8], rewards=[item("minecraft:crafting_table", 1), xp_levels(2)],
        size=1.5, shape="hexagon", subtitle="Storage",
    )
    add(
        s, sl, 10, B, 10, 2.5, "pipez:item_pipe",
        "Item Pipes",
        goal(
            "Craft &632 Pipez item pipes&r.",
            "Chest-to-chest logistics with filters — simpler than Create belts for bulk sorting.",
            tip="Configure with a wrench. Upgrades raise speed.",
        ),
        task_count=32,
        deps=[3], rewards=[item("minecraft:iron_ingot", 16), item("pipez:wrench", 1)],
        subtitle="Pipes",
    )
    add(
        s, sl, 11, B, 12.5, 2.5, "pipez:fluid_pipe",
        "Fluid Pipes",
        goal(
            "Craft &616 fluid pipes&r.",
            "Move water, lava, chocolate, diesel, and Create fluids between tanks and machines.",
        ),
        task_count=16,
        deps=[10], rewards=[item("minecraft:copper_ingot", 16), xp_levels(1)],
        subtitle="Pipes",
    )
    add(
        s, sl, 12, B, 15, 2.5, "pipez:energy_pipe",
        "Energy Pipes",
        goal(
            "Craft &616 energy pipes&r.",
            "Move FE between Create Crafts & Additions machines, jetpack chargers, and electric addons.",
        ),
        task_count=16,
        deps=[11], hide_until_deps=True, rewards=[item("minecraft:redstone", 32)],
        optional=True, subtitle="Pipes",
    )
    add(
        s, sl, 13, B, 15, 0, "ironchest:gold_chest",
        "Gold Chest",
        goal(
            "Upgrade to a Gold Chest.",
            "When drawer networks aren't enough for mixed junk storage.",
        ),
        deps=[9], hide_until_deps=True, rewards=[item("minecraft:gold_ingot", 16)],
        optional=True, subtitle="Storage",
    )
    add(
        s, sl, 14, B, 15, -2.5, "ironfurnaces:gold_furnace",
        "Gold Furnace",
        goal(
            "Craft a Gold Furnace.",
            "Big smelting speed jump. Diamond / netherite tiers wait in Beyond Brass.",
        ),
        deps=[13], hide_until_deps=True, rewards=[item("minecraft:gold_ingot", 16), item("minecraft:coal_block", 4)],
        optional=True, subtitle="Smelting",
    )
    add(
        s, sl, 15, B, 2.5, -2.5, "silentgear:blueprint_paper",
        "Blueprint Paper",
        goal(
            "Craft &64 Silent Gear blueprint papers&r.",
            "Blueprints let you stamp modular tool recipes. Mix materials for mining speed, durability, and harvest level.",
        ),
        task_count=4,
        deps=[2], rewards=[item("silentgear:template_board", 4), xp_levels(1)],
        subtitle="Gear",
    )
    add(
        s, sl, 16, B, 5, -4.5, "silentgear:pickaxe_blueprint",
        "Pickaxe Blueprint",
        goal(
            "Craft a Silent Gear pickaxe blueprint.",
            "Build modular pickaxes — head, rod, and tip materials each matter.",
            tip="JEI shows material traits. Upgrade tips as you find better metals.",
        ),
        deps=[15], rewards=[item("minecraft:iron_ingot", 16), xp_levels(1)],
        subtitle="Gear",
    )
    add(
        s, sl, 17, B, 7.5, -4.5, "silentgear:sword_blueprint",
        "Sword Blueprint",
        goal(
            "Craft a Silent Gear sword blueprint.",
            "Optional combat path — match materials to your mining set for style points.",
        ),
        deps=[16], hide_until_deps=True, rewards=[item("minecraft:iron_sword", 1)],
        optional=True, subtitle="Gear",
    )
    add(
        s, sl, 18, B, 10, -4.5, "constructionstick:iron_stick",
        "Construction Stick",
        goal(
            "Craft an Iron Construction Stick.",
            "Extend walls and platforms in one click — faster base building before Building Gadgets.",
        ),
        deps=[1], rewards=[item("minecraft:iron_ingot", 16)],
        subtitle="Building",
    )
    add(
        s, sl, 19, B, 12.5, -4.5, "buildinggadgets2:gadget_building",
        "Building Gadget",
        goal(
            "Craft a Building Gadget 2.",
            "Copy / build / exchange blocks in bulk — perfect for factories and railways.",
            tip="Exchanging and copy-paste gadgets are worth unlocking next.",
        ),
        deps=[18], rewards=[item("minecraft:redstone", 32), xp_levels(2)],
        size=1.5, subtitle="Building",
    )
    add(
        s, sl, 20, B, 15, -4.5, "buildinggadgets2:gadget_copy_paste",
        "Copy-Paste Gadget",
        goal(
            "Craft the Copy-Paste Gadget.",
            "Save a structure and stamp it elsewhere — repeated factory modules become trivial.",
        ),
        deps=[19], hide_until_deps=True, rewards=[item("buildinggadgets2:template", 1), xp_levels(1)],
        optional=True, subtitle="Building",
    )
    add(
        s, sl, 21, B, 17.5, 0, "artifacts:umbrella",
        "Artifact Hunt",
        goal(
            "Find an Artifacts umbrella (or any artifact you prefer — umbrella is the checklist item).",
            "Trinkets drop from chests, mobs, and exploration. Equip them in Curios slots.",
            tip="Truly optional scavenger hunt — skip if RNG hates you.",
        ),
        deps=[2], hide_until_deps=True, rewards=[item("minecraft:phantom_membrane", 4), xp_levels(2)],
        optional=True, subtitle="Trinkets",
    )
    add(
        s, sl, 22, B, 17.5, 2.5, "minecraft:ender_eye",
        "Structure Scout",
        goal(
            "Craft an Eye of Ender.",
            "Stronghold energy is optional this early — mostly a reminder that &6Lootr&r makes structure chests per-player.",
            tip="Raid structures with friends without loot drama.",
        ),
        deps=[21], hide_until_deps=True, rewards=[item("minecraft:emerald", 8), xp_levels(1)],
        optional=True, subtitle="Exploration",
    )
    add(
        s, sl, 23, B, 17.5, -2.5, "supplementaries:faucet",
        "Faucet",
        goal(
            "Craft a Supplementaries faucet.",
            "Pour fluids from tanks/cauldrons — handy QoL beside Create pumps.",
        ),
        deps=[8], hide_until_deps=True, rewards=[item("supplementaries:jar", 4)],
        optional=True, subtitle="QoL",
    )

    # Refined Storage: a guided, end-to-end network build. The final steps
    # deliberately cover every RS addon shipped by the pack.
    rs_steps = [
        (24, "refinedstorage:quartz_enriched_iron", "Quartz-Enriched Iron", 16,
         "Craft &616 Quartz-Enriched Iron&r.",
         "This is Refined Storage's base material. Keep quartz, iron, redstone, and silicon processing close to your factory.",
         "Batch the processor ingredients now; every network device uses them.", "Core", None),
        (25, "refinedstorage:controller", "Network Controller", 1,
         "Craft and power a Refined Storage Controller.",
         "The Controller is the network heart. Feed it FE from a Create Crafts & Additions alternator, diesel setup, or another generator.",
         "A lit controller means the network has power; every connected device consumes some FE.", "Core", 24),
        (26, "refinedstorage:cable", "Run the Network", 32,
         "Craft &632 Refined Storage cables&r.",
         "Cables join every RS device into one network. Route them behind walls and under Create machines for clean service corridors.",
         "Devices can touch directly; use cable only where you need distance.", "Core", 25),
        (27, "refinedstorage:disk_drive", "Disk Drive", 1,
         "Craft a Disk Drive and connect it to the Controller.",
         "A drive holds up to eight item or fluid disks. It provides bays, not capacity—the disks do that.",
         "Keep spare bays for fluid and Extra Disks upgrades.", "Items", 26),
        (28, "refinedstorage:16k_storage_disk", "16K Item Disk", 1,
         "Craft a 16K Item Storage Disk and place it in the drive.",
         "Item disks store many item types without chest-slot juggling. Upgrade through 64K before entering addon capacities.",
         "Use a Disk Manipulator later to migrate contents between tiers safely.", "Items", 27),
        (29, "refinedstorage:grid", "Storage Grid", 1,
         "Craft a Grid and connect it to the network.",
         "The Grid is the unified view of every disk and attached external inventory. Search, insert, and extract from one screen.",
         "Build the Crafting Grid next so stored ingredients are usable directly.", "Access", 28),
        (30, "refinedstorage:crafting_grid", "Crafting Grid + JEI", 1,
         "Upgrade to a Crafting Grid.",
         "The official RS JEI integration lets JEI transfer recipe ingredients into this grid from network storage.",
         "Open a JEI recipe and press the transfer button; missing ingredients stay highlighted.", "JEI addon", 29),
        (31, "refinedstorage:4096b_fluid_storage_disk", "Fluid Storage", 1,
         "Craft a 4096B Fluid Storage Disk.",
         "RS 2 shows items and fluids in the same Grid. Insert filled containers, or move fluids with importers and exporters.",
         "One bucket equals one bucket of disk capacity; reserve space before automating bulk liquids.", "Fluids", 30),
        (32, "refinedstorage:external_storage", "Expose Create Storage", 2,
         "Craft &62 External Storage devices&r.",
         "Attach one to a Create Item Vault, Functional Storage controller, chest, or fluid tank so RS can use it without copying contents onto disks.",
         "Set priorities: high-priority drawers receive bulk items before general-purpose disks.", "Create integration", 31),
        (33, "refinedstorage:importer", "Import Factory Output", 2,
         "Craft &62 Importers&r.",
         "An Importer pulls items or fluids from an adjacent inventory or tank into RS—ideal on the output buffer of a Create processing line.",
         "Add speed and stack upgrades for high-throughput crushing or washing lines.", "Create integration", 32),
        (34, "refinedstorage:exporter", "Export Ingredients", 2,
         "Craft &62 Exporters&r.",
         "An Exporter keeps selected items or fluids supplied to an adjacent machine, basin buffer, deployer chest, or Create tank.",
         "Use regulator upgrades when a machine should hold an exact stock instead of being flooded.", "Create integration", 33),
        (35, "refinedstorage:interface", "Factory Interface", 2,
         "Craft &62 Interfaces&r.",
         "Interfaces expose filtered stock to outside automation. Create funnels, chutes, arms, belts, and Pipez can interact with their slots.",
         "Use interfaces as clean hand-off points between the digital network and physical factory logistics.", "Outside automation", 34),
        (36, "refinedstorage:pattern_grid", "Pattern Grid", 1,
         "Craft a Pattern Grid.",
         "Encode crafting recipes and processing recipes onto patterns. Processing patterns describe inputs sent out and outputs expected back.",
         "Use processing patterns for Create crushing, mixing, pressing, deploying, and sequenced assembly.", "Autocrafting", 35),
        (37, "refinedstorage:pattern", "Encode Patterns", 8,
         "Craft &68 blank Patterns&r and encode useful recipes.",
         "Start with common components, then encode Create processes. Put crafting patterns and processing patterns into the right autocrafters.",
         "Test one processing step before chaining a long production request.", "Autocrafting", 36),
        (38, "refinedstorage:autocrafter", "Autocrafter", 2,
         "Craft &62 Autocrafters&r.",
         "Autocrafters execute patterns. Point processing outputs toward an Interface so RS can detect returned products and finish the job.",
         "The Autocrafter Manager helps organize large walls of patterns.", "Autocrafting", 37),
        (39, "refinedstorage:wireless_transmitter", "Wireless Transmitter", 1,
         "Craft a Wireless Transmitter.",
         "Connect it to the network and install range upgrades to reach across your base.",
         "Wireless access still consumes network power and has a configured range.", "Wireless", 38),
        (40, "refinedstorage:wireless_grid", "Wireless Grid + Curios", 1,
         "Craft and link a Wireless Grid.",
         "The official Curios integration adds dedicated RS slots, letting a linked portable or wireless grid travel equipped outside your inventory.",
         "Use the linking tool on the network, charge the grid, then equip it in its Curios slot.", "Curios addon", 39),
        (41, "extradisks:1024k_item_storage_disk", "Extra Disks: 1024K", 1,
         "Craft a 1024K Item Storage Disk from Extra Disks.",
         "Extra Disks extends RS with enormous item and fluid tiers for mature factories. Upgrade gradually instead of crafting infinite storage early.",
         "Withering processors gate the highest tiers behind Nether progression.", "Extra Disks addon", 40),
        (42, "extrastorage:advanced_importer", "Advanced Importer", 1,
         "Craft an ExtraStorage Advanced Importer.",
         "Its larger filter and higher throughput suit multi-output Create farms and processing arrays.",
         "Filter explicitly so valuable outputs never loop back into the wrong line.", "ExtraStorage addon", 41),
        (43, "extrastorage:advanced_exporter", "Advanced Exporter", 1,
         "Craft an ExtraStorage Advanced Exporter.",
         "Use the expanded filter to stock several ingredients at a shared factory input buffer.",
         "Pair it with a Create belt or mechanical arm to distribute ingredients physically.", "ExtraStorage addon", 42),
        (44, "extrastorage:netherite_crafter", "Netherite Crafter", 1,
         "Craft ExtraStorage's Netherite Crafter.",
         "This top-tier crafter holds more patterns and processes requests faster—ideal for a dense late-game pattern hall.",
         "Spread processing recipes across crafters when several Create lines can run in parallel.", "ExtraStorage addon", 43),
        (45, "extrastorage:disk_1048576b_fluid", "Million-Bucket Fluid Disk", 1,
         "Craft ExtraStorage's 1,048,576B Fluid Storage Disk.",
         "Use this endgame tank for diesel products, liquid experience, chocolate, honey, lava, or any other factory-scale fluid.",
         "External Storage is still better when you want the fluid visibly stored in Create tanks.", "ExtraStorage addon", 44),
    ]

    for n, task, title, count, what, body, tip, subtitle, dep in rs_steps:
        add(
            s, sl, n, B,
            (n - 24) % 11 * 2.5,
            7.0 + ((n - 24) // 11) * 2.5,
            task,
            title,
            goal(what, body, tip=tip),
            task_count=count,
            deps=[dep] if dep is not None else None,
            links=[C_PRECISION] if n == 24 else None,
            rewards=[xp_levels(2 if n >= 36 else 1)],
            size=1.5 if n in {25, 30, 38, 40, 45} else 1.0,
            shape="hexagon" if n in {30, 40, 45} else None,
            subtitle=subtitle,
        )

    return s, sl


def chapter_automation(add: QuestAdder) -> tuple[list[dict], dict[str, dict]]:
    a: list[dict] = []
    al: dict[str, dict] = {}
    B = 400

    add(
        a, al, 0, B, 0, 0, "integrateddynamics:menril_log",
        "Menril Wood",
        goal(
            "Collect &616 menril logs&r.",
            "Menril fuels Integrated Dynamics crafting. Find menril trees / berries in the world (Nature's Compass helps).",
            tip="Crystalized menril chunks also drop — keep them for cables and variables.",
            nxt="Spin up a cable network, then learn variables.",
        ),
        task_count=16,
        links=[C_BRASS], rewards=[item("integrateddynamics:crystalized_menril_chunk", 16), xp_levels(1)],
        size=1.5, subtitle="Integrated Dynamics",
    )
    add(
        a, al, 1, B, 2.5, 0, "integrateddynamics:cable",
        "Logic Network",
        goal(
            "Craft &632 Integrated Dynamics cables&r.",
            "ID is this pack's programmable logistics brain — readers, writers, and terminals plug into cable.",
            tip="Think of cables like a tiny computer bus running through your base.",
        ),
        task_count=32,
        deps=[0], rewards=[item("integrateddynamics:crystalized_menril_chunk", 16), xp_levels(1)],
        size=2.0, shape="gear", subtitle="Integrated Dynamics",
    )
    add(
        a, al, 2, B, 5, 0, "integrateddynamics:logic_programmer",
        "Logic Programmer",
        goal(
            "Craft a Logic Programmer.",
            "The desk where you write variable cards — numbers, items, lists, operators, and filters.",
            tip="There's also a portable programmer for field work.",
        ),
        deps=[1], rewards=[item("integrateddynamics:variable", 16), xp_levels(1)],
        subtitle="Integrated Dynamics",
    )
    add(
        a, al, 3, B, 7.5, 0, "integrateddynamics:variable",
        "Variables",
        goal(
            "Craft &616 variables&r.",
            "Store numbers, items, lists, and logic — programming cards for your network.",
        ),
        task_count=16,
        deps=[2], rewards=[item("integrateddynamics:cable", 8)],
        subtitle="Integrated Dynamics",
    )
    add(
        a, al, 4, B, 10, 0, "integrateddynamics:part_inventory_reader",
        "Inventory Reader",
        goal(
            "Craft an Inventory Reader part.",
            "Attach to a cable facing an inventory to read contents into variables — the eyes of your network.",
        ),
        deps=[3], rewards=[item("integrateddynamics:variable", 8), xp_levels(1)],
        subtitle="Integrated Dynamics",
    )
    add(
        a, al, 5, B, 12.5, 0, "integrateddynamics:part_display_panel",
        "Display Panel",
        goal(
            "Craft a display panel.",
            "Show variable values on the wall — debug your logic without guessing.",
        ),
        deps=[3], hide_until_deps=True, rewards=[item("minecraft:glass_pane", 16)],
        optional=True, subtitle="Integrated Dynamics",
    )
    add(
        a, al, 6, B, 5, 2.5, "integratedtunnels:part_interface_item",
        "Item Tunnels",
        goal(
            "Craft &64 item interfaces&r (Integrated Tunnels).",
            "Pull and push items with filters — ID's version of import/export buses.",
            nxt="Importers automate continuous transfer; terminals let you browse the network.",
        ),
        task_count=4,
        deps=[1], rewards=[item("minecraft:hopper", 4)],
        subtitle="Tunnels",
    )
    add(
        a, al, 7, B, 7.5, 2.5, "integratedtunnels:part_importer_item",
        "Item Importer",
        goal(
            "Craft an item importer.",
            "Continuously pull items into the network with filters and conditions.",
        ),
        deps=[6], rewards=[item("integrateddynamics:variable", 8), xp_levels(1)],
        subtitle="Tunnels",
    )
    add(
        a, al, 8, B, 10, 2.5, "integratedtunnels:part_interface_fluid",
        "Fluid Tunnels",
        goal(
            "Craft &62 fluid interfaces&r.",
            "Move Create fluids, diesel fuels, and liquid XP through the ID network.",
        ),
        task_count=2,
        deps=[6], hide_until_deps=True, rewards=[item("minecraft:bucket", 4)],
        optional=True, subtitle="Tunnels",
    )
    add(
        a, al, 9, B, 7.5, 4.5, "integratedterminals:part_terminal_storage",
        "Storage Terminal",
        goal(
            "Craft a Storage Terminal.",
            "Browse and craft from everything your tunnels can see — the AE2 vibe without AE2.",
            tip="Portable terminal exists for on-the-go access once unlocked.",
        ),
        deps=[7], rewards=[item("minecraft:ender_eye", 4), xp_levels(2)],
        size=1.5, shape="hexagon", subtitle="Terminals",
    )
    add(
        a, al, 10, B, 10, 4.5, "integratedcrafting:part_interface_crafting",
        "Crafting Interface",
        goal(
            "Craft a Crafting Interface.",
            "Request autocrafting through your ID terminal once patterns / recipes are set up.",
            nxt="You're ready for factory-scale enchanting and fuel systems.",
        ),
        deps=[9], rewards=[item("minecraft:crafting_table", 1), xp_levels(2)],
        size=1.5, subtitle="Autocrafting",
    )
    add(
        a, al, 11, B, 2.5, -2.5, "createaddition:alternator",
        "Alternator",
        goal(
            "Build a Create Crafts & Additions Alternator.",
            "Spin it with SU to generate FE (Forge Energy) for electric addons and jetpack charging.",
        ),
        deps=[1], rewards=[item("createaddition:capacitor", 2), xp_levels(1)],
        subtitle="Power",
    )
    add(
        a, al, 12, B, 5, -2.5, "createaddition:electric_motor",
        "Electric Motor",
        goal(
            "Build an Electric Motor.",
            "Turn FE back into SU — great for remote bases powered by diesel or New Age electricity.",
        ),
        deps=[11], rewards=[item("createaddition:copper_spool", 4), xp_levels(1)],
        subtitle="Power",
    )
    add(
        a, al, 13, B, 7.5, -2.5, "createaddition:rolling_mill",
        "Rolling Mill",
        goal(
            "Build a CCA Rolling Mill.",
            "Roll rods and wires for electrical crafting — pairs with the alternator line.",
        ),
        deps=[12], hide_until_deps=True, rewards=[item("minecraft:iron_ingot", 16)],
        optional=True, subtitle="Power",
    )
    add(
        a, al, 14, B, 10, -2.5, "createdieselgenerators:oil_scanner",
        "Oil Scanner",
        goal(
            "Craft an oil scanner (Create Diesel Generators).",
            "Find crude oil deposits before committing to a pumpjack.",
        ),
        deps=[12], rewards=[item("createdieselgenerators:plant_oil_bucket", 2), xp_levels(1)],
        subtitle="Diesel",
    )
    add(
        a, al, 15, B, 12.5, -2.5, "createdieselgenerators:diesel_engine",
        "Diesel Engine",
        goal(
            "Build a Diesel Engine.",
            "Process plant oil / crude into fuel and burn it for strong kinetic power — Create's combustion route.",
            tip="Distillation controller + pumpjacks scale this into a fuel empire.",
        ),
        deps=[14], rewards=[item("createdieselgenerators:engine_piston", 2), xp_levels(2)],
        size=1.5, subtitle="Diesel",
    )
    add(
        a, al, 16, B, 15, -2.5, "createdieselgenerators:distillation_controller",
        "Distillation",
        goal(
            "Craft a distillation controller.",
            "Refine crude into diesel, gasoline, and other fractions for engines and asphalt builds.",
        ),
        deps=[15], hide_until_deps=True, rewards=[item("createdieselgenerators:oil_barrel", 2), xp_levels(1)],
        optional=True, subtitle="Diesel",
    )
    add(
        a, al, 17, B, 12.5, 2.5, "create_enchantment_industry:experience_hatch",
        "Experience Hatch",
        goal(
            "Craft an experience hatch (Enchantment Industry).",
            "Get liquid XP into Create fluid networks — the fuel for automated enchanting.",
        ),
        deps=[9], rewards=[item("minecraft:experience_bottle", 8), xp_levels(1)],
        subtitle="Enchanting",
    )
    add(
        a, al, 18, B, 15, 2.5, "create_enchantment_industry:blaze_enchanter",
        "Blaze Enchanter",
        goal(
            "Build a Blaze Enchanter.",
            "Pump liquid experience and automate enchanted books / gear — factory magic.",
            tip="Printers copy enchanted books once you have templates.",
        ),
        deps=[17], rewards=[item("create_enchantment_industry:enchanting_template", 2), xp_levels(2)],
        size=1.5, subtitle="Enchanting",
    )
    add(
        a, al, 19, B, 17.5, 2.5, "create_enchantment_industry:printer",
        "Enchantment Printer",
        goal(
            "Craft an Enchantment Industry printer.",
            "Copy enchantments onto books/gear with liquid XP — mass-produce your favorite setups.",
        ),
        deps=[18], hide_until_deps=True, rewards=[item("minecraft:book", 16), xp_levels(2)],
        optional=True, subtitle="Enchanting",
    )
    add(
        a, al, 20, B, 15, 4.5, "sliceanddice:slicer",
        "Slice & Dice",
        goal(
            "Craft a Slice & Dice slicer.",
            "Pair with Create to automate Farmer's Delight cutting — salads on a conveyor belt.",
        ),
        deps=[9], hide_until_deps=True, rewards=[item("farmersdelight:cutting_board", 1), xp_levels(1)],
        optional=True, subtitle="Food automation",
    )
    add(
        a, al, 21, B, 17.5, 4.5, "sliceanddice:sprinkler",
        "Sprinkler",
        goal(
            "Craft a Slice & Dice sprinkler.",
            "Automate crop hydration / fertilizer vibes for bigger farms.",
        ),
        deps=[20], hide_until_deps=True, rewards=[item("minecraft:bone_meal", 32)],
        optional=True, subtitle="Food automation",
    )
    add(
        a, al, 22, B, 17.5, -2.5, "create_connected:brake",
        "Kinetic Brake",
        goal(
            "Craft a Brake (Create: Connected).",
            "Connected adds practical kinetic utilities — brakes, clutches, copycats-adjacent helpers, and more.",
        ),
        deps=[11], hide_until_deps=True, rewards=[item("create:electron_tube", 2), xp_levels(1)],
        optional=True, subtitle="Create extras",
    )
    add(
        a, al, 23, B, 12.5, -4.5, "create_connected:parallel_gearbox",
        "Parallel Gearbox",
        goal(
            "Craft a parallel gearbox (Create: Connected).",
            "Compact kinetic routing for dense factory floors — squeeze more shafts into less space.",
        ),
        deps=[22], hide_until_deps=True, rewards=[item("create:cogwheel", 8)],
        optional=True, subtitle="Create extras",
    )

    # Powah: generation, transmission, energizing tiers, reactors, and
    # wireless power. This branch can power Refined Storage independently or
    # exchange FE with Create through Crafts & Additions.
    powah_steps = [
        (24, "powah:dielectric_paste", "Dielectric Beginnings", 16,
         "Craft &616 Dielectric Paste&r.",
         "Powah uses dielectric paste, rods, and casings throughout every generator and storage tier.",
         "Cook it in batches; upgrading machines repeatedly consumes plenty.", "Materials", None),
        (25, "powah:furnator_starter", "Starter Furnator", 1,
         "Craft a Starter Furnator.",
         "Burn solid fuel for your first independent FE supply—enough to bootstrap Refined Storage and the Energizing Orb.",
         "Set output sides in the GUI or connect an energy cable.", "Generation", 24),
        (26, "powah:energy_cable_starter", "Starter Energy Cables", 16,
         "Craft &616 Starter Energy Cables&r.",
         "Powah cables move FE between generators, cells, RS controllers, chargers, and Create Crafts & Additions machines.",
         "Upgrade the cable tier when transfer rate becomes the bottleneck.", "Transfer", 25),
        (27, "powah:energy_cell_starter", "Starter Energy Cell", 1,
         "Craft a Starter Energy Cell.",
         "Cells buffer generation so machines survive demand spikes and generators can keep working between jobs.",
         "Place storage between generation and the factory bus.", "Storage", 26),
        (28, "powah:thermo_generator_starter", "Thermo Generator", 1,
         "Craft a Starter Thermo Generator.",
         "Place it above a hot block and supply water for passive, fuel-free FE. Better heat sources improve output.",
         "Use a sink or pumped Create tank for reliable water supply.", "Generation", 27),
        (29, "powah:magmator_starter", "Magmator", 1,
         "Craft a Starter Magmator.",
         "A Magmator consumes lava for steady power—an excellent match for Create hose pulleys and train-delivered lava.",
         "Buffer lava in a Create Fluid Tank before feeding the generator.", "Generation", 28),
        (30, "powah:solar_panel_starter", "Solar Panel", 1,
         "Craft a Starter Solar Panel.",
         "Solar panels generate free daytime power with clear sky access. Combine sources rather than relying on one generator.",
         "Store daytime surplus in an Energy Cell for overnight use.", "Generation", 28),
        (31, "powah:energizing_orb", "Energizing Orb", 1,
         "Craft an Energizing Orb.",
         "The Orb turns ordinary materials into Powah's tier crystals when Energizing Rods supply enough FE.",
         "Items can be inserted and removed with Create funnels, deployers, arms, Pipez, or RS interfaces.", "Energizing", 27),
        (32, "powah:energizing_rod_starter", "Energizing Rod", 2,
         "Craft &62 Starter Energizing Rods&r.",
         "Point rods at the Orb with an unobstructed line of sight. More and better rods deliver recipes faster.",
         "Connect every rod to the same buffered power network.", "Energizing", 31),
        (33, "powah:steel_energized", "Energized Steel", 8,
         "Produce &68 Energized Steel&r.",
         "This first energized material unlocks Basic-tier generators, cables, cells, batteries, and wireless devices.",
         "Encode the Orb recipe in Refined Storage once your processing autocrafting is ready.", "Tier: Basic", 32),
        (34, "powah:crystal_blazing", "Blazing Crystal", 8,
         "Produce &68 Blazing Crystals&r.",
         "Blazing tier raises generation, capacity, and transfer rates with Nether materials.",
         "Keep blaze products automated with a Create farm or bulk processing line.", "Tier: Blazing", 33),
        (35, "powah:crystal_niotic", "Niotic Crystal", 8,
         "Produce &68 Niotic Crystals&r.",
         "Niotic power uses diamonds and marks the jump into serious factory-scale FE.",
         "Upgrade bottlenecks together: generator, cell, and cable throughput.", "Tier: Niotic", 34),
        (36, "powah:crystal_spirited", "Spirited Crystal", 8,
         "Produce &68 Spirited Crystals&r.",
         "Spirited tier is an emerald-heavy late-game step suited to large RS autocrafting networks.",
         "Only upgrade machines whose capacity or rate you actually need.", "Tier: Spirited", 35),
        (37, "powah:crystal_nitro", "Nitro Crystal", 4,
         "Produce &64 Nitro Crystals&r.",
         "Nitro is Powah's top survival tier and requires Nether Stars plus a major FE investment.",
         "A buffered reactor network prevents the energizing operation from starving your base.", "Tier: Nitro", 36),
        (38, "powah:uraninite", "Uraninite Supply", 16,
         "Process &616 Uraninite&r.",
         "Uraninite fuels Powah reactors. Mine its ore and energize or smelt it before building sustained reactor power.",
         "Stock coal, redstone, water, and dry ice too; reactors perform best with all required inputs.", "Reactors", 33),
        (39, "powah:reactor_starter", "Starter Reactor", 1,
         "Craft and assemble a Starter Reactor.",
         "Reactors compactly generate continuous FE from uraninite and supporting resources. Configure inputs before enabling full production.",
         "Automate each consumable and send output through an Energy Cell.", "Reactors", 38),
        (40, "powah:reactor_nitro", "Nitro Reactor", 1,
         "Upgrade all the way to a Nitro Reactor.",
         "This is the endgame Powah generator: enormous output for RS autocrafting, jetpacks, and electrically driven Create factories.",
         "Monitor fuel and cooling; huge theoretical output is useless without automated supply.", "Reactors", 37),
        (41, "powah:ender_cell_starter", "Ender Cell", 1,
         "Craft a Starter Ender Cell.",
         "Ender Cells store power in a frequency-based wireless network shared by linked Ender Gates.",
         "Use separate channels for public infrastructure and critical machines.", "Wireless network", 33),
        (42, "powah:ender_gate_starter", "Ender Gate", 2,
         "Craft &62 Starter Ender Gates&r.",
         "Attach gates to distant machines for cable-free FE access through the selected Ender Cell channel.",
         "A gate's transfer limit still depends on its tier.", "Wireless network", 41),
        (43, "powah:player_transmitter_starter", "Player Transmitter", 1,
         "Craft a Starter Player Transmitter.",
         "Player Transmitters wirelessly charge carried equipment—especially Iron Jetpacks and Powah batteries.",
         "Bind yourself with the correct card and keep the transmitter supplied with FE.", "Wireless charging", 42),
        (44, "powah:battery_starter", "Portable Battery", 1,
         "Craft a Starter Battery.",
         "A battery carries FE between jobs and provides a simple test item for your Player Transmitter.",
         "Upgrade its tier alongside your wireless charging rate and equipment demand.", "Wireless charging", 43),
    ]

    for n, task, title, count, what, body, tip, subtitle, dep in powah_steps:
        add(
            a, al, n, B,
            (n - 24) % 11 * 2.5,
            7.0 + ((n - 24) // 11) * 2.5,
            task,
            title,
            goal(what, body, tip=tip),
            task_count=count,
            deps=[dep] if dep is not None else None,
            links=[C_BRASS] if n == 24 else None,
            rewards=[xp_levels(2 if n >= 33 else 1)],
            size=1.5 if n in {25, 31, 39, 40, 43} else 1.0,
            shape="hexagon" if n in {31, 40, 43} else None,
            subtitle=f"Powah · {subtitle}",
        )

    # RFTools: use Powah as the energy backbone, then progress through general
    # automation, remote storage, teleportation, and RF-powered dimensions.
    rftools_steps = [
        (45, "rftoolsbase:machine_frame", "RFTools Framework", 4,
         "Craft &64 RFTools Machine Frames&r.",
         "Machine Frames are the common chassis for the entire RFTools suite.",
         "Keep a batch in Refined Storage; nearly every branch consumes them.", "Foundation", None),
        (46, "rftoolsbase:smartwrench", "Smart Wrench", 1,
         "Craft an RFTools Smart Wrench.",
         "The wrench rotates, configures, links, and safely moves through RFTools setups.",
         "Carry it before placing machines whose facing or links matter.", "Tools", 45),
        (47, "rftoolspower:coalgenerator", "Coal Generator", 1,
         "Craft an RFTools Coal Generator.",
         "This compact generator is a fallback FE source and a clear introduction to RFTools Power.",
         "Feed the same power bus as Powah, but let Powah handle serious base generation.", "Power", 45),
        (48, "rftoolspower:cell1", "Power Cell", 1,
         "Craft a Level 1 Power Cell.",
         "Power Cells buffer FE locally and can grow into linked power networks.",
         "Place one beside bursty machines so cable demand stays smooth.", "Power", 47),
        (49, "rftoolspower:powercell_card", "Powercell Card", 1,
         "Craft a Powercell Card.",
         "Cards link compatible RFTools power cells and dimensional cells into a shared network.",
         "Name cards or networks by purpose to avoid cross-wiring factories.", "Power networking", 48),
        (50, "rftoolspower:dimensionalcell", "Dimensional Cell", 1,
         "Craft a Dimensional Cell.",
         "Dimensional Cells move FE across distance and dimensions without running physical cables.",
         "Use Powah generation to charge the network that supports teleporters and dimensions.", "Power networking", 49),
        (51, "rftoolsutility:crafter1", "Automated Crafter", 1,
         "Craft a Tier 1 RFTools Crafter.",
         "RFTools Crafters continuously process buffered recipes, ideal for compact material loops.",
         "Use Create or Pipez to supply ingredients and export results to Refined Storage.", "Automation", 45),
        (52, "rftoolsutility:crafter3", "Tier 3 Crafter", 1,
         "Upgrade to a Tier 3 RFTools Crafter.",
         "The top crafter handles many recipes in one block and can retain intermediates internally.",
         "Use remembered outputs carefully to prevent recipe loops from clogging.", "Automation", 51),
        (53, "rftoolsutility:screen", "Information Screen", 1,
         "Craft an RFTools Screen.",
         "Screens present power, inventory, fluid, machine, and text data through installable modules.",
         "Build the module that matches the system you actually need to monitor.", "Monitoring", 45),
        (54, "rftoolsutility:screen_controller", "Screen Controller", 1,
         "Craft a Screen Controller.",
         "A controller supplies power and data to nearby screens for a clean factory dashboard.",
         "Keep its range and FE use in mind when laying out a control room.", "Monitoring", 53),
        (55, "rftoolspower:power_monitor", "Power Monitor", 1,
         "Craft a Power Monitor.",
         "Monitor stored energy and emit redstone at useful thresholds before the factory browns out.",
         "Connect the signal to backup Powah generators or nonessential machine shutoffs.", "Monitoring", 54),
        (56, "rftoolsutility:matter_transmitter", "Matter Transmitter", 1,
         "Craft a Matter Transmitter.",
         "Matter transmitters send players to linked receivers and form the travel backbone of RFTools Dimensions.",
         "Teleportation needs reliable FE; buffer it rather than trusting live generation.", "Teleportation", 50),
        (57, "rftoolsutility:matter_receiver", "Matter Receiver", 1,
         "Craft a Matter Receiver.",
         "A receiver creates a destination for transmitters, including in distant or custom dimensions.",
         "Power and protect the destination before dialing it.", "Teleportation", 56),
        (58, "rftoolsutility:dialing_device", "Dialing Device", 1,
         "Craft a Dialing Device.",
         "The dialer discovers nearby transmitters and receivers and connects the selected route.",
         "Give destinations clear names so travel remains safe and predictable.", "Teleportation", 57),
        (59, "rftoolsutility:environmental_controller", "Environmental Controller", 1,
         "Craft an Environmental Controller.",
         "With modules installed, this powered machine applies useful effects across a configurable area.",
         "Its ongoing FE cost rises with range and modules, so measure before expanding.", "Utility", 50),
        (60, "rftoolsstorage:storage_module1", "Storage Module", 1,
         "Craft a Tier 1 Storage Module.",
         "Storage Modules determine the capacity of Modular Storage blocks.",
         "This is complementary local storage; keep bulk searchable stock in Refined Storage.", "Storage", 45),
        (61, "rftoolsstorage:modular_storage", "Modular Storage", 1,
         "Craft Modular Storage and install your module.",
         "One compact block exposes the module's inventory with filtering and a convenient interface.",
         "Use it for work cells whose contents should stay separate from the main network.", "Storage", 60),
        (62, "rftoolsstorage:storage_scanner", "Storage Scanner", 1,
         "Craft a Storage Scanner.",
         "The scanner searches and accesses nearby inventories from one interface without replacing them.",
         "Scan Create vaults and local chests, then use RS for globally managed storage.", "Storage", 61),
        (63, "rftoolsstorage:tablet_scanner", "Remote Storage Tablet", 1,
         "Craft a Storage Scanner Tablet.",
         "The tablet gives portable access to a linked scanner when it has power and connectivity.",
         "Keep it charged with Powah wireless charging before long expeditions.", "Storage", 62),
        (64, "rftoolsstorage:crafting_manager", "Crafting Manager", 1,
         "Craft an RFTools Crafting Manager.",
         "The manager coordinates RFTools storage and crafting resources from a central interface.",
         "Use it for self-contained production cells; RS remains best for pack-wide autocrafting.", "Storage automation", 63),
        (65, "rftoolsbase:dimensionalshard", "Dimensional Shards", 8,
         "Collect &68 Dimensional Shards&r.",
         "These rare materials gate advanced RFTools machinery and the custom-dimension path.",
         "Check JEI's ore-height display and dimension sources before committing to a mining trip.", "Dimensions", 58),
        (66, "rftoolsdim:dimlet_workbench", "Dimlet Workbench", 1,
         "Craft a Dimlet Workbench.",
         "The workbench assembles researched parts into dimlets that describe terrain, biomes, blocks, and features.",
         "Start with a simple, low-cost world before combining expensive effects.", "Dimensions", 65),
        (67, "rftoolsdim:researcher", "Dimlet Researcher", 1,
         "Craft a Dimlet Researcher.",
         "Research turns lost knowledge into usable information for building custom dimlets.",
         "Automate its inputs only after understanding the rarity tiers.", "Dimensions", 66),
        (68, "rftoolsdim:enscriber", "Dimension Enscriber", 1,
         "Craft a Dimension Enscriber.",
         "The Enscriber combines selected dimlets with a dimension tab to define a realizable world.",
         "Read the projected maintenance cost and avoid unstable combinations.", "Dimensions", 67),
        (69, "rftoolsdim:dimension_builder", "Dimension Builder", 1,
         "Craft a Dimension Builder.",
         "The Builder realizes and continuously powers your designed dimension.",
         "Supply a large Powah/RFTools energy buffer, then place a powered receiver before exploring.", "Dimensions", 68),
    ]

    for n, task, title, count, what, body, tip, subtitle, dep in rftools_steps:
        add(
            a, al, n, B,
            (n - 45) % 13 * 2.5,
            12.5 + ((n - 45) // 13) * 2.5,
            task,
            title,
            goal(what, body, tip=tip),
            task_count=count,
            deps=[dep] if dep is not None else None,
            links=[B + 27] if n == 45 else None,
            rewards=[xp_levels(2 if n >= 65 else 1)],
            size=1.5 if n in {45, 50, 52, 58, 62, 69} else 1.0,
            shape="hexagon" if n in {50, 58, 69} else None,
            subtitle=f"RFTools · {subtitle}",
        )

    # Flux Networks: a universal wireless FE layer that connects Powah,
    # RFTools, Refined Storage, and electrically powered Create machinery.
    flux_steps = [
        (70, "fluxnetworks:flux_dust", "Flux from Bedrock", 16,
         "Produce &616 Flux Dust&r.",
         "Flux Dust is the foundation of a wireless FE network and is created through its special bedrock interaction recipe.",
         "Check JEI for the exact in-world process; bring enough redstone for a batch.", "Materials", None),
        (71, "fluxnetworks:flux_core", "Flux Cores", 8,
         "Craft &68 Flux Cores&r.",
         "Cores turn Flux Dust into network devices and storage components.",
         "Keep them stocked in Refined Storage for future expansion.", "Components", 70),
        (72, "fluxnetworks:flux_block", "Flux Block", 4,
         "Craft &64 Flux Blocks&r.",
         "Flux Blocks compress network material and are used by the more capable devices.",
         "Automate dust and core production before building at scale.", "Components", 71),
        (73, "fluxnetworks:flux_plug", "Flux Plug", 1,
         "Craft a Flux Plug.",
         "A Plug takes FE from an attached generator, cell, or machine and inserts it into your selected wireless network.",
         "Attach it to the output side of Powah or RFTools storage, then set a transfer limit.", "Wireless input", 72),
        (74, "fluxnetworks:flux_point", "Flux Point", 1,
         "Craft a Flux Point.",
         "A Point extracts FE from the network into Refined Storage, RFTools, or Create Crafts & Additions machines.",
         "Use priorities and limits so one hungry machine cannot starve the entire base.", "Wireless output", 73),
        (75, "fluxnetworks:flux_configurator", "Flux Configurator", 1,
         "Craft a Flux Configurator.",
         "The Configurator makes network-device management quicker while building and troubleshooting.",
         "Name networks by purpose and use security settings on multiplayer servers.", "Network tools", 74),
        (76, "fluxnetworks:flux_controller", "Flux Controller", 1,
         "Craft a Flux Controller.",
         "Controllers provide central network management and enable wireless charging for players and selected equipment.",
         "Review chunk loading, transfer bypass, and member permissions rather than enabling everything blindly.", "Network control", 75),
        (77, "fluxnetworks:basic_flux_storage", "Basic Flux Storage", 1,
         "Craft Basic Flux Storage.",
         "Network storage absorbs surplus generation and covers demand spikes without extra cables.",
         "Keep a physical Powah or RFTools buffer too, so critical machines have layered resilience.", "Energy storage", 74),
        (78, "fluxnetworks:herculean_flux_storage", "Herculean Storage", 1,
         "Upgrade to Herculean Flux Storage.",
         "Herculean storage supports factory-scale reserves for autocrafting, teleportation, and dimension upkeep.",
         "Watch actual input and output rates; capacity alone does not solve a generation shortage.", "Energy storage", 77),
        (79, "fluxnetworks:gargantuan_flux_storage", "Gargantuan Storage", 1,
         "Craft Gargantuan Flux Storage.",
         "The largest survival Flux storage tier is an endgame reservoir for a fully wireless power grid.",
         "Feed it with automated high-tier Powah generation and monitor it from your RFTools control room.", "Energy storage", 78),
    ]

    for n, task, title, count, what, body, tip, subtitle, dep in flux_steps:
        add(
            a, al, n, B,
            (n - 70) * 2.5,
            18.0,
            task,
            title,
            goal(what, body, tip=tip),
            task_count=count,
            deps=[dep] if dep is not None else None,
            links=[B + 50] if n == 70 else None,
            rewards=[xp_levels(2 if n >= 76 else 1)],
            size=1.5 if n in {73, 74, 76, 79} else 1.0,
            shape="hexagon" if n in {76, 79} else None,
            subtitle=f"Flux Networks · {subtitle}",
        )

    return a, al


def chapter_late(add: QuestAdder) -> tuple[list[dict], dict[str, dict]]:
    l: list[dict] = []
    ll: dict[str, dict] = {}
    B = 500

    add(
        l, ll, 0, B, 0, 0, "minecraft:netherite_ingot",
        "Netherite",
        goal(
            "Smith a netherite ingot.",
            "Ancient debris + gold. The late-game material gate for this book — furnaces, sticks, and flex.",
            tip="Bring fire resistance, a Waystone, and dignity.",
            nxt="Flight, trains, cannons, and the finale bosses await.",
        ),
        links=[C_PRECISION], rewards=[item("minecraft:ancient_debris", 4), xp_levels(3)],
        size=2.0, shape="gear", subtitle="Endgame gate",
    )
    add(
        l, ll, 1, B, 2.5, 0, "ironfurnaces:netherite_furnace",
        "Netherite Furnace",
        goal(
            "Craft a Netherite Furnace.",
            "Top-tier smelting speed for when your ore drill finally wakes up.",
        ),
        deps=[0], rewards=[item("minecraft:netherite_ingot", 1), xp_levels(2)],
        subtitle="Smelting",
    )
    add(
        l, ll, 2, B, 2.5, 2.5, "ironchest:obsidian_chest",
        "Obsidian Chest",
        goal(
            "Craft an Obsidian Chest.",
            "Blast-resistant storage for bases that… experiment with Big Cannons.",
        ),
        deps=[1], hide_until_deps=True, rewards=[item("minecraft:obsidian", 32)],
        optional=True, subtitle="Storage",
    )
    add(
        l, ll, 3, B, 2.5, -2.5, "ironchest:diamond_chest",
        "Diamond Chest",
        goal(
            "Craft a Diamond Chest.",
            "Huge mixed storage before full digital networks take over.",
        ),
        deps=[1], hide_until_deps=True, rewards=[item("minecraft:diamond", 8)],
        optional=True, subtitle="Storage",
    )
    add(
        l, ll, 4, B, 5, 0, "ironjetpacks:thruster",
        "Jetpack Thrusters",
        goal(
            "Craft &62 Iron Jetpacks thrusters&r.",
            "Combine with coils, capacitors, cells, and a strap to assemble modular jetpacks.",
            tip="Charge with FE from your alternator / diesel / New Age setup.",
        ),
        task_count=2,
        deps=[0], rewards=[item("ironjetpacks:basic_coil", 2), xp_levels(1)],
        subtitle="Flight",
    )
    add(
        l, ll, 5, B, 7.5, 0, "ironjetpacks:cell",
        "Jetpack Cell",
        goal(
            "Craft an Iron Jetpacks energy cell.",
            "Energy storage for your jetpack assembly — don't skip the battery.",
        ),
        deps=[4], rewards=[item("ironjetpacks:capacitor", 1)],
        subtitle="Flight",
    )
    add(
        l, ll, 6, B, 10, 0, "ironjetpacks:jetpack",
        "Iron Jetpack",
        goal(
            "Assemble an Iron Jetpacks jetpack.",
            "Charge it and take to the skies — independent from Create backtanks.",
        ),
        deps=[5], rewards=[xp_levels(3)],
        size=1.5, shape="hexagon", subtitle="Flight",
    )
    add(
        l, ll, 7, B, 5, -2.5, "create_jetpack:jetpack",
        "Create Jetpack",
        goal(
            "Craft the Create Jetpack.",
            "Runs off copper backtank pressure — perfect if your factory already fills tanks.",
        ),
        deps=[6], rewards=[item("create:copper_backtank", 1), xp_levels(2)],
        size=1.5, subtitle="Flight",
    )
    add(
        l, ll, 8, B, 7.5, -2.5, "create_sa:brass_jetpack_chestplate",
        "Brass Jetpack",
        goal(
            "Craft Stuff 'N Additions brass jetpack chestplate.",
            "Another flight option for brass-rich factories — pick your favorite sky kit.",
        ),
        deps=[7], hide_until_deps=True, rewards=[item("create:brass_ingot", 16), xp_levels(2)],
        optional=True, subtitle="Flight",
    )
    add(
        l, ll, 9, B, 5, 2.5, "createbigcannons:cannon_mount",
        "Cannon Mount",
        goal(
            "Craft a Create Big Cannons mount.",
            "The base of a buildable cannon. Build responsibly. Or don't. We put it in the pack either way.",
            tip="Foundries and cast moulds make proper barrels — JEI is your friend.",
        ),
        deps=[14], hide_until_deps=True, rewards=[item("minecraft:iron_block", 4), xp_levels(1)],
        optional=True, subtitle="Chaos",
    )
    add(
        l, ll, 10, B, 7.5, 2.5, "createbigcannons:solid_shot",
        "Solid Shot",
        goal(
            "Craft solid shot ammunition.",
            "Optional gunnery goal — test ranges strongly recommended.",
        ),
        deps=[9], hide_until_deps=True, rewards=[item("minecraft:gunpowder", 16)],
        optional=True, subtitle="Chaos",
    )
    add(
        l, ll, 11, B, 10, 2.5, "create:track",
        "Rail Empire",
        goal(
            "Craft &664 Create tracks&r.",
            "Link factories across the map. Trains move bulk ore, fuel, and players.",
        ),
        task_count=64,
        deps=[0], links=[C_TRACK], rewards=[item("create:precision_mechanism", 2), xp_levels(2)],
        subtitle="Trains",
    )
    add(
        l, ll, 12, B, 12.5, 2.5, "railways:conductor_whistle",
        "Conductor Whistle",
        goal(
            "Craft a Steam 'n' Rails conductor whistle.",
            "Conductors, fancy tracks, and train QoL — run the railway like you mean it.",
        ),
        deps=[11], rewards=[item("railways:fuel_tank", 1), xp_levels(2)],
        subtitle="Trains",
    )
    add(
        l, ll, 13, B, 15, 2.5, "bellsandwhistles:headlight",
        "Train Headlight",
        goal(
            "Craft a Bells & Whistles headlight.",
            "Dress up locomotives — pilots, grab rails, metro casing, and station flair.",
        ),
        deps=[12], hide_until_deps=True, rewards=[item("bellsandwhistles:metro_casing", 8)],
        optional=True, subtitle="Trains",
    )
    add(
        l, ll, 14, B, 12.5, 0, "create:precision_mechanism",
        "Mechanism Stockpile",
        goal(
            "Stockpile &632 precision mechanisms&r.",
            "If this hurts, your assembly line isn't automated enough yet — go fix that.",
            tip="Mechanical crafters + deployers + arms should be feeding a chest nonstop.",
        ),
        task_count=32,
        deps=[6], links=[C_PRECISION], rewards=[item("create:brass_sheet", 32), xp_levels(3)],
        size=1.5, subtitle="Logistics flex",
    )
    add(
        l, ll, 15, B, 15, 0, "minecraft:nether_star",
        "Wither Down",
        goal(
            "Defeat the Wither and hold a nether star.",
            "Beacon bases make Create factories feel unfair in the best way — haste + speed while building is cracked.",
        ),
        deps=[14], rewards=[item("minecraft:diamond_block", 2), xp_levels(5)],
        size=1.75, shape="pentagon", subtitle="Boss",
    )
    add(
        l, ll, 16, B, 17.5, 0, "minecraft:dragon_egg",
        "Dragon Egg",
        goal(
            "Claim the dragon egg after beating the Ender Dragon.",
            "Trophy of the End. Keep it safe — or display it above the factory.",
        ),
        deps=[15], hide_until_deps=True, rewards=[item("minecraft:end_crystal", 4), xp_levels(3)],
        optional=True, size=1.5, subtitle="Boss",
    )
    add(
        l, ll, 17, B, 20, 0, "minecraft:elytra",
        "Elytra",
        goal(
            "Claim elytra from the End.",
            "Combine with a jetpack or fireworks — you're done with walking.",
            "You've reached the end of the guided quest book. Keep building absurd factories, railways, and questionable cannons.",
            tip="Shulker shells turn storage portable. Firework rockets are still valid tech.",
        ),
        deps=[15], rewards=[
            item("minecraft:firework_rocket", 64),
            item("minecraft:shulker_shell", 4),
            xp_levels(5),
        ],
        size=2.0, shape="gear", subtitle="Finale",
    )
    add(
        l, ll, 18, B, 12.5, -2.5, "constructionstick:netherite_stick",
        "Netherite Construction Stick",
        goal(
            "Craft the netherite construction stick.",
            "Maximum reach building for megabases and rail yards.",
        ),
        deps=[1], hide_until_deps=True, rewards=[xp_levels(2)],
        optional=True, subtitle="Building",
    )
    add(
        l, ll, 19, B, 15, -2.5, "tombstone:grave_dust",
        "Tombstone Dust",
        goal(
            "Collect &68 grave dust&r from Corail Tombstone.",
            "Graves protect your items on death — dust feeds magic crafts. Die less; collect more.",
        ),
        task_count=8,
        deps=[0], hide_until_deps=True, rewards=[item("minecraft:bone", 32), xp_levels(1)],
        optional=True, subtitle="Death QoL",
    )
    add(
        l, ll, 20, B, 17.5, -2.5, "create_sa:brass_drill_head",
        "Brass Drill Head",
        goal(
            "Craft a brass drill head (Stuff 'N Additions).",
            "Extra Create tools for excavation-style play — optional flex craft.",
        ),
        deps=[14], hide_until_deps=True, rewards=[item("create:brass_ingot", 8)],
        optional=True, subtitle="Tools",
    )
    add(
        l, ll, 21, B, 10, -4.5, "minecraft:beacon",
        "Beacon Base",
        goal(
            "Craft a beacon.",
            "Power it with your nether star. Haste II while placing Create shafts is a lifestyle.",
        ),
        deps=[15], hide_until_deps=True, rewards=[item("minecraft:iron_block", 36), xp_levels(2)],
        optional=True, subtitle="Boss",
    )

    return l, ll


def build_all(add: QuestAdder) -> dict[str, tuple[list[dict], dict[str, dict]]]:
    return {
        "foundations": chapter_foundations(add),
        "create_factory": chapter_create(add),
        "storage_gear": chapter_storage(add),
        "automation": chapter_automation(add),
        "late_game": chapter_late(add),
    }
