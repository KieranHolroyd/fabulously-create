"""11. Extreme Reactors quest chapter."""
from __future__ import annotations

from ftb_quests.ast import Chapter, Quest, require, xp_levels
from ftb_quests.ids import A_ALTERNATOR
from ftb_quests.text import overview, tutorial


def chapter() -> Chapter:
    return Chapter(
        key='extreme_reactors',
        base=700,
        chapter_id='A20000000000000C',
        icon='bigreactors:basic_reactorcontroller',
        title='11. Extreme Reactors',
        subtitle='Yellorium reactors, steam turbines, and fuel reprocessing',
        quests=[
            Quest(
                n=0,
                x=0.0,
                y=0.0,
                task='bigreactors:yellorium_ingot',
                title='Yellorium',
                desc=overview(
                    "Extreme Reactors turns yellorium into FE — first as a small passive reactor, "
                    "then as an actively cooled steam loop into a turbine. This chapter walks you "
                    "from ore to ludicrite endgame.",
                    you_will=[
                        "Mine yellorite and stock graphite for reactor parts",
                        "Build a hollow Basic reactor with fuel rods, control rods, and a power tap",
                        "Graduate to active cooling, turbines, cyanite reprocessing, and Reinforced tier",
                    ],
                    tip="Start tiny. A 5×5×5 outer shell (~3×3×3 interior) teaches the layout before you scale.",
                )
                + [""]
                + tutorial(
                    "Smelt &616 Yellorium Ingots&r.",
                    why="Yellorium is the fuel metal every Basic reactor burns. Without a stockpile, "
                    "your first controller is just a fancy doorstop.",
                    steps=[
                        "Hunt &6Yellorite Ore&r underground (deepslate variants count). Nature's Compass won't find it — dig, explore, or filter a Digital Miner.",
                        "Smelt the ore into &eYellorium Ingots&r and keep extras for fuel rods plus later crafts.",
                    ],
                    tip="Batch-smelt; inserting fuel and crafting parts both chew through ingots.",
                    nxt="Graphite next — casings and rods need it in bulk.",
                ),
                task_count=16,
                links=require(A_ALTERNATOR),
                rewards=[xp_levels(1)],
                size=1.5,
                subtitle='Extreme Reactors · Fuel',
            ),
            Quest(
                n=1,
                x=2.5,
                y=0.0,
                task='bigreactors:graphite_ingot',
                title='Graphite Bars',
                desc=tutorial(
                    "Craft &616 Graphite Bars&r.",
                    why="Graphite shows up in casings, fuel rods, control rods, and turbine parts. "
                    "Treat it like a second fuel supply for the whole chapter.",
                    steps=[
                        "Open JEI for &6Graphite Bar&r — charcoal, coal coke, or similar carbon routes depending on the pack.",
                        "Craft a chestful and park it next to your reactor build site.",
                    ],
                    tip="Running out mid-shell is painful; overshoot on the first batch.",
                    nxt="Casings form the hollow reactor shell.",
                ),
                task_count=16,
                deps=[0],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Materials',
            ),
            Quest(
                n=2,
                x=5.0,
                y=0.0,
                task='bigreactors:basic_reactorcasing',
                title='Reactor Casing',
                desc=tutorial(
                    "Craft &624 Basic Reactor Casings&r.",
                    why="Casings (and glass) make the hollow cuboid shell. Controllers, ports, and taps "
                    "replace face blocks later — corners must always stay casing.",
                    steps=[
                        "Pick a starter footprint: outer &e5×5×5&r (about &e3×3×3&r interior) is ideal. Basic reactors top out near &e5×5×5&r interior — don't max it on day one.",
                        "Build a hollow cuboid: floor, walls, and ceiling of &6Basic Reactor Casing&r. Leave the interior empty air.",
                        "Corners and edges must be casing. You can swap some wall faces for reactor glass once you craft it — never the corners.",
                    ],
                    tip="Frame the shell first, then punch holes for the controller, power tap, and access port.",
                    nxt="The controller validates the multiblock.",
                ),
                task_count=24,
                deps=[1],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=3,
                x=7.5,
                y=0.0,
                task='bigreactors:basic_reactorcontroller',
                title='Reactor Controller',
                desc=tutorial(
                    "Craft a Basic Reactor Controller.",
                    why="The controller is the brain — it assembles the multiblock and shows heat, fuel, "
                    "reactivity, and power. No valid controller, no reactor.",
                    steps=[
                        "Replace one face block (not a corner) with the &6Basic Reactor Controller&r.",
                        "Stand back and confirm the structure assembles (outline / GUI). If it fails, check hollow interior, casing corners, and that only valid reactor parts sit on the shell.",
                        "Leave room on other faces for a &ePower Tap&r and &eAccess Port&r — don't cover every wall with glass yet.",
                    ],
                    tip="Controller on the front face, ports on the sides keeps cable runs tidy.",
                    nxt="Fuel rods go in interior columns under control rods.",
                ),
                deps=[2],
                rewards=[xp_levels(1)],
                size=1.5,
                shape='hexagon',
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=4,
                x=10.0,
                y=0.0,
                task='bigreactors:basic_reactorfuelrod',
                title='Fuel Rods',
                desc=tutorial(
                    "Craft &64 Basic Reactor Fuel Rods&r.",
                    why="Fuel rods hold yellorium inside the hollow core. Each column of rods is one "
                    "fuel channel — more rods means more heat and power, and more waste.",
                    steps=[
                        "Inside the hollow volume, place vertical columns of &6Basic Reactor Fuel Rods&r from floor level up toward the ceiling.",
                        "Start with one or two short columns — four rods is plenty for a first reactor.",
                        "Leave the block directly above each column free for a &eControl Rod&r (next quest).",
                    ],
                    tip="Don't pack the entire interior on the first build; learn heat before you scale.",
                    nxt="Control rods sit on top of each fuel column.",
                ),
                task_count=4,
                deps=[3],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=5,
                x=12.5,
                y=0.0,
                task='bigreactors:basic_reactorcontrolrod',
                title='Control Rods',
                desc=tutorial(
                    "Craft &62 Basic Reactor Control Rods&r.",
                    why="Control rods cap each fuel column and let you throttle reactivity from the "
                    "controller GUI. Insertion high = cooler, safer startup.",
                    steps=[
                        "Place a &6Basic Reactor Control Rod&r in the ceiling / top face directly above each fuel-rod column.",
                        "Confirm every fuel column has a matching control rod — orphan rods won't moderate properly.",
                        "Before inserting fuel, set insertion high (nearly fully inserted) so the first light-off stays gentle.",
                    ],
                    tip="Always throttle with rods before you add more fuel rods later.",
                    nxt="A passive power tap pulls FE without a turbine.",
                ),
                task_count=2,
                deps=[4],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=6,
                x=15.0,
                y=0.0,
                task='bigreactors:basic_reactorpowertapfe_passive',
                title='Power Tap',
                desc=tutorial(
                    "Craft a Basic Passive FE Power Tap.",
                    why="Passive cooling dumps heat as FE through a power tap — the simplest Extreme "
                    "Reactors setup. Active cooling (steam out → turbine) comes later for much higher output.",
                    steps=[
                        "Replace a face casing (not a corner) with the &6Passive FE Power Tap&r.",
                        "Connect energy cables / conduits from the tap to a battery or your factory bus.",
                        "Insert yellorium through an access port (next) or by hand, then slowly withdraw control rods while watching heat in the controller.",
                    ],
                    tip="If heat climbs faster than your cables can drain, push rods back in before you expand.",
                    nxt="Access ports automate fuel in and cyanite out.",
                ),
                deps=[5],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=7,
                x=17.5,
                y=0.0,
                task='bigreactors:basic_reactorsolidaccessport',
                title='Access Port',
                desc=tutorial(
                    "Craft a Basic Solid Access Port.",
                    why="The solid access port is how yellorium enters and cyanite waste leaves. "
                    "Automate it early so you aren't hand-feeding a hot core.",
                    steps=[
                        "Replace another face block with the &6Basic Solid Access Port&r.",
                        "Configure the port for fuel input / waste output, then pipe yellorium in and cyanite out with item pipes or transporters.",
                        "With port, tap, controller, fuel columns, and control rods in place, light the reactor and confirm FE on the tap.",
                    ],
                    tip="Cyanite stacks up fast — chest it or send it toward the reprocessor branch.",
                    nxt="Two paths open: collect cyanite, or start the turbine line for active cooling.",
                ),
                deps=[6],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Reactor',
            ),
            Quest(
                n=8,
                x=0.0,
                y=2.5,
                task='bigreactors:cyanite_ingot',
                title='Cyanite Waste',
                desc=tutorial(
                    "Collect &68 Cyanite Ingots&r.",
                    why="Burned yellorium becomes cyanite. It's not trash — reprocessing turns waste "
                    "into the next fuel tier toward blutonium and ludicrite.",
                    steps=[
                        "Run the reactor until spent fuel ejects as &6Cyanite&r through the access port.",
                        "Pull eight ingots into your inventory (or a chest the quest can see).",
                        "Stockpile the rest; the reprocessor will want a steady feed.",
                    ],
                    tip="Don't void cyanite if you care about the endgame fuel ladder.",
                    nxt="Craft the reprocessor controller when you're ready to recycle.",
                ),
                task_count=8,
                deps=[7],
                rewards=[xp_levels(1)],
                subtitle='Extreme Reactors · Fuel cycle',
            ),
            Quest(
                n=9,
                x=2.5,
                y=2.5,
                task='bigreactors:basic_turbinecasing',
                title='Turbine Housing',
                desc=tutorial(
                    "Craft &620 Basic Turbine Housings&r.",
                    why="Active cooling vents steam from the reactor into a turbine multiblock. "
                    "Steam → rotor → coils makes far more FE than a passive power tap alone.",
                    steps=[
                        "Build a hollow turbine shell from &6Basic Turbine Housing&r — leave room for a central rotor shaft, blades, coils, and a bearing.",
                        "Plan fluid ports: steam in from the reactor (or a steam buffer), water/condensate out.",
                        "Keep the turbine near the reactor so steam pipes stay short.",
                    ],
                    tip="Switch the reactor to active cooling only after the turbine shell and ports are ready.",
                    nxt="The turbine controller assembles the multiblock.",
                ),
                task_count=20,
                deps=[7],
                rewards=[xp_levels(2)],
                subtitle='Extreme Reactors · Turbine',
            ),
            Quest(
                n=10,
                x=5.0,
                y=2.5,
                task='bigreactors:basic_turbinecontroller',
                title='Turbine Controller',
                desc=tutorial(
                    "Craft a Basic Turbine Controller.",
                    why="The controller validates the turbine and exposes RPM, steam intake, and "
                    "energy output. Tune coil and blade counts from here.",
                    steps=[
                        "Place the &6Basic Turbine Controller&r on a housing face (not a corner).",
                        "Add a rotor bearing, a straight &eRotor Shaft&r down the axis, and leave space for blades and inductive coils around/along the design JEI shows.",
                        "Mount fluid ports for steam intake and water exhaust, plus a power tap for FE out.",
                    ],
                    tip="Match blades and coils to your steam supply — overspeed or under-coiled rotors waste efficiency.",
                    nxt="Rotor blades catch the steam flow.",
                ),
                deps=[9],
                rewards=[xp_levels(2)],
                size=1.5,
                subtitle='Extreme Reactors · Turbine',
            ),
            Quest(
                n=11,
                x=7.5,
                y=2.5,
                task='bigreactors:basic_turbinerotorblade',
                title='Rotor Blades',
                desc=tutorial(
                    "Craft &68 Basic Turbine Rotor Blades&r.",
                    why="Blades on the rotor convert steam flow into shaft RPM. Coils then turn that "
                    "spin into FE — balance both sides of the machine.",
                    steps=[
                        "Attach &6Rotor Blades&r along the shaft per the turbine layout (pairs of blades on shaft segments).",
                        "Install inductive coils in their designated coil region so RPM produces energy instead of free-spinning.",
                        "Feed steam, watch RPM in the controller, and adjust blade/coil count if intake and induction don't match.",
                    ],
                    tip="Too many blades without coils stalls; too many coils without blades underproduce.",
                    nxt="Meanwhile, recycle cyanite in the reprocessor.",
                ),
                task_count=8,
                deps=[10],
                rewards=[xp_levels(2)],
                subtitle='Extreme Reactors · Turbine',
            ),
            Quest(
                n=12,
                x=10.0,
                y=2.5,
                task='bigreactors:reprocessorcontroller',
                title='Cyanite Reprocessor',
                desc=tutorial(
                    "Craft a Reprocessor Controller.",
                    why="The cyanite reprocessor multiblock turns waste back into useful fuel feedstocks "
                    "for the next tier — required if you want blutonium and ludicrite.",
                    steps=[
                        "Build the reprocessor shell from its casings (JEI / Patchouli list every part).",
                        "Place the &6Collector&r on the bottom center and the &6Waste Injector&r on the top center.",
                        "Put power, fluid, and output ports on the sides; pipe cyanite into the injector and pull products from the output.",
                        "Power the machine and run a small cyanite batch to confirm the loop before you scale the reactor.",
                    ],
                    tip="Keep a buffer chest between the reactor access port and the waste injector.",
                    nxt="Reinforced parts unlock larger, hotter cores.",
                ),
                deps=[8],
                rewards=[xp_levels(2)],
                subtitle='Extreme Reactors · Fuel cycle',
            ),
            Quest(
                n=13,
                x=12.5,
                y=2.5,
                task='bigreactors:reinforced_reactorcontroller',
                title='Reinforced Reactor',
                desc=tutorial(
                    "Craft a Reinforced Reactor Controller.",
                    why="Reinforced reactors dwarf Basic size limits, handle hotter fuels, and pair "
                    "with serious turbine loops. Upgrade when Basic heat or footprint is the bottleneck — "
                    "not before cyanite recycling is stable.",
                    steps=[
                        "Craft the &6Reinforced Reactor Controller&r and matching reinforced casings / rods as JEI shows.",
                        "Build a larger hollow cuboid the same way: casing corners, hollow interior, fuel columns with control rods on top, ports on faces.",
                        "Move to active cooling + turbine if you haven't already — Reinforced output will swamp a lone passive tap.",
                    ],
                    caution="Bigger cores melt faster when cooling or rod control lags. Commission cool before you fill every fuel column.",
                    tip="Migrate your access-port automation and waste line before the first Reinforced light-off.",
                    nxt="Ludicrite is the bragging-rights endgame metal.",
                ),
                deps=[12],
                rewards=[xp_levels(2)],
                size=1.5,
                shape='hexagon',
                subtitle='Extreme Reactors · Endgame',
            ),
            Quest(
                n=14,
                x=15.0,
                y=2.5,
                task='bigreactors:ludicrite_ingot',
                title='Ludicrite',
                desc=tutorial(
                    "Craft &64 Ludicrite Ingots&r.",
                    why="Ludicrite is Extreme Reactors' endgame material — top-tier components and "
                    "proof your fuel cycle (cyanite → blutonium → ludicrite) actually works.",
                    steps=[
                        "Follow JEI for &6Ludicrite&r — blutonium from reprocessing plus End-dimension or other gated ingredients typically appear.",
                        "Keep the reprocessor fed so blutonium doesn't become the bottleneck mid-craft.",
                        "Craft four ingots and stash spares for any ludicrite-tier parts you still want.",
                    ],
                    tip="If a ingredient looks alien, check the End and your cyanite stocks first.",
                ),
                task_count=4,
                deps=[13],
                rewards=[xp_levels(2)],
                subtitle='Extreme Reactors · Endgame',
            ),
        ],
    )
