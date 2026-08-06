"""10. Mekanism Reactors quest chapter."""
from __future__ import annotations

from ftb_quests.ast import Chapter, Quest, require, xp_levels
from ftb_quests.ids import MEKANISM_START
from ftb_quests.text import overview, tutorial


def chapter() -> Chapter:
    return Chapter(
        key='mekanism_generators',
        base=650,
        chapter_id='A20000000000000B',
        icon='mekanismgenerators:fission_reactor_casing',
        title='10. Mekanism Reactors',
        subtitle='Heat, solar, wind, fission, turbines, and fusion power',
        quests=[
            Quest(
                n=0,
                x=0.0,
                y=0.0,
                task='mekanismgenerators:heat_generator',
                title='Heat Generator',
                desc=overview(
                    "Mekanism Generators climbs from lava-side heat and rooftop solar up through "
                    "fission, industrial turbines, and fusion ignition. Wire each step before you "
                    "touch nuclear fuel.",
                    you_will=[
                        "Bootstrap FE with heat, solar, wind, bio, and gas-burning generators",
                        "Assemble a water-cooled fission reactor and spin an Industrial Turbine",
                        "Frame a fusion reactor, load a Hohlraum, and ignite with lasers",
                    ],
                    tip="Buffer every generator into an Energy Cube — nuclear lessons are easier with spare FE.",
                )
                + [""]
                + tutorial(
                    "Craft a Heat Generator.",
                    why="The Heat Generator is your first Mekanism FE — burn solid fuel or park it "
                    "beside lava for quiet bootstrap power while steel casings and circuits come online.",
                    steps=[
                        "Craft the &6Heat Generator&r and place it next to lava (or feed it solid fuel in the GUI).",
                        "Set an output side and pull FE with a Universal Cable into a Basic Energy Cube.",
                        "Keep the cube charged so Metallurgic Infusers and early machines never brown out.",
                    ],
                    tip="Lava-adjacent heat is steady and fuel-free once the pool is safe.",
                    nxt="Solar covers daytime loads without babysitting fuel.",
                ),
                links=require(MEKANISM_START),
                rewards=[xp_levels(1)],
                size=1.5,
                subtitle='Mekanism Generators · Early power',
            ),
            Quest(
                n=1,
                x=2.5,
                y=0.0,
                task='mekanismgenerators:solar_generator',
                title='Solar Generator',
                desc=tutorial(
                    "Craft &62 Solar Generators&r.",
                    why="Solar is silent daytime FE with zero fuel logistics. Pair it with storage so "
                    "night shifts still run enrichment and crushing.",
                    steps=[
                        "Craft two &6Solar Generators&r and place them with a clear view of the sky.",
                        "Cable both into the same Energy Cube (or Induction Matrix later).",
                        "Confirm daytime charge in the cube GUI — if night drains you dry, add more panels or cubes before expanding machines.",
                    ],
                    tip="Advanced Solar (later) covers a 3×3 footprint for a big jump in output.",
                    nxt="Wind keeps producing after sunset.",
                ),
                task_count=2,
                deps=[0],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Early power',
            ),
            Quest(
                n=2,
                x=5.0,
                y=0.0,
                task='mekanismgenerators:wind_generator',
                title='Wind Generator',
                desc=tutorial(
                    "Craft a Wind Generator.",
                    why="Wind scales with height and runs day and night — perfect rooftop power once "
                    "your factory has a tall enough tower.",
                    steps=[
                        "Craft a &6Wind Generator&r and place it high above the base (clear air around the rotor).",
                        "Open the GUI after placing — higher Y-level means more FE/t.",
                        "Cable it into your cube bus alongside solar so nights stay covered.",
                    ],
                    tip="Scaffold a dedicated wind tower; burying the generator at ground level wastes potential.",
                    nxt="Bio-fuel is the compact fuel-based option.",
                ),
                deps=[1],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Early power',
            ),
            Quest(
                n=3,
                x=7.5,
                y=0.0,
                task='mekanismgenerators:bio_generator',
                title='Bio-Generator',
                desc=tutorial(
                    "Craft a Bio-Generator.",
                    why="Bio-Generators burn bio fuel refined from organic matter — dense FE when you "
                    "already farm crops or compost leftovers.",
                    steps=[
                        "Craft the &6Bio-Generator&r and place it near your farm or compost line.",
                        "Produce &eBio Fuel&r (Crusher / enrichment routes — check JEI) and pipe or insert it into the generator.",
                        "Wire FE out to the same cube network as solar and wind.",
                    ],
                    tip="A small crop farm beats coal runs once the bio loop is automatic.",
                    nxt="Gas-burning turns electrolyzed hydrogen into serious FE.",
                ),
                deps=[1],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Early power',
            ),
            Quest(
                n=4,
                x=10.0,
                y=0.0,
                task='mekanismgenerators:gas_burning_generator',
                title='Gas-Burning Generator',
                desc=tutorial(
                    "Craft a Gas-Burning Generator.",
                    why="Burn hydrogen (and other burnable gases) from an Electrolytic Separator for "
                    "dense FE that scales with your water and power budget.",
                    steps=[
                        "Set up an &6Electrolytic Separator&r with water input; collect &eHydrogen&r in a gas tank or pressurized tube.",
                        "Place the &6Gas-Burning Generator&r and pipe hydrogen in with Pressurized Tubes.",
                        "Cable FE out — surplus electrolysis power often pays for itself once the loop is closed.",
                    ],
                    tip="Dump oxygen or store it; don't let gas backups stall the separator.",
                    nxt="Fission starts with a lot of casing — stock up first.",
                ),
                deps=[3],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Gas power',
            ),
            Quest(
                n=5,
                x=12.5,
                y=0.0,
                task='mekanismgenerators:advanced_solar_generator',
                title='Advanced Solar',
                desc=tutorial(
                    "Craft an Advanced Solar Generator.",
                    why="Advanced Solar is a mid-game array — much higher daytime output before you "
                    "commit to fission logistics and radiation planning.",
                    steps=[
                        "Craft the &6Advanced Solar Generator&r (it needs a 3×3 clear footprint).",
                        "Place it with open sky, cable into an Energy Cube or Induction Matrix.",
                        "Use the buffer to ride through night and brownouts while you prep fission parts.",
                    ],
                    tip="Still daylight-gated — matrices beat a pile of small cubes for nuclear prep.",
                    nxt="Fission casings build the hollow reactor shell.",
                ),
                deps=[2],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Early power',
            ),
            Quest(
                n=6,
                x=15.0,
                y=0.0,
                task='mekanismgenerators:fission_reactor_casing',
                title='Fission Casing',
                desc=tutorial(
                    "Craft &632 Fission Reactor Casings&r.",
                    why="Fission is a hollow cuboid of casing, ports, fuel assemblies, and control rods. "
                    "Water cools the core; heated coolant and nuclear waste come out the other side — "
                    "plan containment before the first assembly goes in.",
                    steps=[
                        "Choose a starter size (small hollow cuboid) and gather &632 Fission Reactor Casings&r plus glass/ports as JEI shows.",
                        "Build a hollow shell: casing floor, walls, and ceiling with air inside. Corners and edges must form correctly or the multiblock fails.",
                        "Leave face slots open for &eFission Reactor Ports&r; interior space must fit fuel assemblies and control rod assemblies above them.",
                    ],
                    caution="Fission leaks radiation when things go wrong. Build away from living areas and keep a Geiger Counter handy.",
                    tip="Use the multiblock overlay — missing corners and solid interiors are the usual formation killers.",
                    nxt="Fuel assemblies hold fissile fuel inside the shell.",
                ),
                task_count=32,
                deps=[4],
                rewards=[xp_levels(1)],
                size=1.5,
                shape='hexagon',
                subtitle='Mekanism Generators · Fission',
            ),
            Quest(
                n=7,
                x=17.5,
                y=0.0,
                task='mekanismgenerators:fission_fuel_assembly',
                title='Fuel Assemblies',
                desc=tutorial(
                    "Craft &64 Fission Fuel Assemblies&r.",
                    why="Fuel assemblies are the interior columns that hold &6Fissile Fuel&r. More "
                    "assemblies raise heat and steam potential — and meltdown risk if cooling lags.",
                    steps=[
                        "Place vertical &6Fission Fuel Assemblies&r inside the hollow casing, leaving the top of each column free for a control rod assembly.",
                        "Start with a few assemblies only — four is a teaching core, not a megabase.",
                        "Produce &eFissile Fuel&r through the Mekanism processing line before you plan to run; never light an empty or uncooled core.",
                    ],
                    tip="Add assemblies only after coolant flow and waste barrels are proven.",
                    nxt="Control rods sit above the fuel columns.",
                ),
                task_count=4,
                deps=[6],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Fission',
            ),
            Quest(
                n=8,
                x=0.0,
                y=2.5,
                task='mekanismgenerators:control_rod_assembly',
                title='Control Rods',
                desc=tutorial(
                    "Craft &62 Control Rod Assemblies&r.",
                    why="Control rod assemblies throttle the reaction from the fission GUI (and redstone "
                    "/ logic adapters). Enough rods let you SCRAM if heat spikes.",
                    steps=[
                        "Place a &6Control Rod Assembly&r directly above each fuel-assembly column (through the ceiling as the multiblock requires).",
                        "Confirm formation, then keep rods inserted until coolant and waste ports are connected.",
                        "Optionally wire a Logic Adapter for emergency insertion from redstone or industrial alarms.",
                    ],
                    tip="Never run with rods yanked out 'to see what happens' — heat climbs fast.",
                    nxt="Ports move coolant, heated coolant, fuel, and waste.",
                ),
                task_count=2,
                deps=[7],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Fission',
            ),
            Quest(
                n=9,
                x=2.5,
                y=2.5,
                task='mekanismgenerators:fission_reactor_port',
                title='Fission Ports',
                desc=tutorial(
                    "Craft &62 Fission Reactor Ports&r.",
                    why="Ports are the only safe way to inject coolant and pull heated coolant / waste. "
                    "Without a planned loop, the reactor cooks itself and radiates the chunk.",
                    steps=[
                        "Replace face casings with &6Fission Reactor Ports&r and configure modes: coolant in (water), heated coolant out, waste out, fuel in as needed.",
                        "Pipe &ewater&r coolant in and route &eheated coolant&r toward a Thermoelectric Boiler (or equivalent) that makes steam for the Industrial Turbine.",
                        "Barrel or pipe &enuclear waste&r to safe storage immediately — never dump it into the world.",
                        "Activate only after coolant flow is continuous; watch burn rate and heat, ready to insert rods.",
                    ],
                    caution="Meltdowns and waste mishandling spread radiation. Wear a Hazmat Suit and keep scrap / absorbent supplies ready.",
                    tip="Prove the coolant loop on a short run before you scale fuel assemblies.",
                    nxt="Turbine casings turn that steam into FE.",
                ),
                task_count=2,
                deps=[8],
                rewards=[xp_levels(1)],
                subtitle='Mekanism Generators · Fission',
            ),
            Quest(
                n=10,
                x=5.0,
                y=2.5,
                task='mekanismgenerators:turbine_casing',
                title='Industrial Turbine',
                desc=tutorial(
                    "Craft &624 Turbine Casings&r.",
                    why="The Industrial Turbine converts steam into massive FE. Fission (via boiler) "
                    "or other steam sources feed it — this is the payoff for the nuclear loop.",
                    steps=[
                        "Build a hollow turbine structure from &6Turbine Casings&r with room for a rotor shaft, blades, vents, condensers, and electromagnetic coils.",
                        "Add a turbine valve / steam input from your boiler and plan water return from condensers so the coolant loop can close.",
                        "Leave coil and blade space clear — stuffing the interior with casing blocks prevents formation.",
                    ],
                    tip="Match turbine size to steam supply; a giant empty turbine won't invent pressure.",
                    nxt="Blades set how much steam the rotor can catch.",
                ),
                task_count=24,
                deps=[9],
                rewards=[xp_levels(2)],
                size=1.5,
                subtitle='Mekanism Generators · Turbine',
            ),
            Quest(
                n=11,
                x=7.5,
                y=2.5,
                task='mekanismgenerators:turbine_blade',
                title='Turbine Blades',
                desc=tutorial(
                    "Craft &68 Turbine Blades&r.",
                    why="Blades on the rotor shaft set flow capacity. Undersized vents choke output; "
                    "oversized blade stacks without steam waste materials.",
                    steps=[
                        "Install &6Turbine Blades&r on the rotor shaft segments inside the casing.",
                        "Add pressure dispersers / vents as the multiblock guide requires so steam can expand across the blades.",
                        "Spin up with a modest steam feed and confirm RPM / production before maxing blade count.",
                    ],
                    tip="Balance blades, vents, and condensers — any weak link caps FE.",
                    nxt="Electromagnetic coils turn rotor motion into energy.",
                ),
                task_count=8,
                deps=[10],
                rewards=[xp_levels(2)],
                subtitle='Mekanism Generators · Turbine',
            ),
            Quest(
                n=12,
                x=10.0,
                y=2.5,
                task='mekanismgenerators:electromagnetic_coil',
                title='Electromagnetic Coils',
                desc=tutorial(
                    "Craft &62 Electromagnetic Coils&r.",
                    why="Coils convert rotor spin into FE. More coils raise energy production for a "
                    "given steam flow once vents and condensers keep up.",
                    steps=[
                        "Place &6Electromagnetic Coils&r in the coil layer of the turbine multiblock.",
                        "Add saturating condensers to reclaim water and close the loop back to your boiler / fission coolant circuit.",
                        "Cable FE from the turbine's energy output into an Induction Matrix — fission spikes will saturate small cubes.",
                    ],
                    tip="If production plateaus, check steam feed and vent count before crafting more coils.",
                    nxt="Fusion is the endgame — start framing next.",
                ),
                task_count=2,
                deps=[11],
                rewards=[xp_levels(2)],
                subtitle='Mekanism Generators · Turbine',
            ),
            Quest(
                n=13,
                x=12.5,
                y=2.5,
                task='mekanismgenerators:fusion_reactor_frame',
                title='Fusion Frame',
                desc=tutorial(
                    "Craft &616 Fusion Reactor Frames&r.",
                    why="Fusion is Mekanism's endgame power: a framed reactor burns deuterium–tritium "
                    "fuel after laser ignition. Stock frames, ports, and cooling before you chase a Hohlraum.",
                    steps=[
                        "Craft &616 Fusion Reactor Frames&r and gather the matching ports, glass, and controller parts from JEI.",
                        "Build the hollow fusion reactor structure — frames form the skeleton; leave faces for the controller, ports, and laser focus access.",
                        "Prepare &eDeuterium&r and &eTritium&r production (heavy water / gas processing lines) so ignition isn't starved for fuel.",
                    ],
                    tip="Budget serious FE for the laser charging step — weak grids fail ignition awkwardly.",
                    nxt="The fusion controller is the multiblock brain.",
                ),
                task_count=16,
                deps=[12],
                rewards=[xp_levels(2)],
                subtitle='Mekanism Generators · Fusion',
            ),
            Quest(
                n=14,
                x=15.0,
                y=2.5,
                task='mekanismgenerators:fusion_reactor_controller',
                title='Fusion Controller',
                desc=tutorial(
                    "Craft a Fusion Reactor Controller.",
                    why="The controller assembles the fusion multiblock and shows heat, fuel injection, "
                    "and status. Water cooling and steam extraction can feed the same turbine network as fission.",
                    steps=[
                        "Place the &6Fusion Reactor Controller&r on a valid face and confirm the reactor forms.",
                        "Configure ports for D-T fuel injection and coolant / steam handling.",
                        "Build or aim a &6Laser Focus Matrix&r (and amplifiers) at the reactor — ignition needs a charged laser pulse, not just filled tanks.",
                    ],
                    tip="Dial injection rates slowly after the first successful burn; runaway heat still punishes greed.",
                    nxt="Load a Hohlraum to light the first sustained reaction.",
                ),
                deps=[13],
                rewards=[xp_levels(2)],
                size=1.5,
                shape='hexagon',
                subtitle='Mekanism Generators · Fusion',
            ),
            Quest(
                n=15,
                x=17.5,
                y=2.5,
                task='mekanismgenerators:hohlraum',
                title='Hohlraum',
                desc=tutorial(
                    "Craft a Hohlraum.",
                    why="A Hohlraum loaded with fusion fuel is what the laser ignites. Failed starts "
                    "and restarts consume them — keep spares on the shelf.",
                    steps=[
                        "Craft a &6Hohlraum&r and fill it with the fusion fuel mix JEI / the reactor GUI expects (D-T).",
                        "Insert the loaded Hohlraum into the fusion reactor per the controller interface.",
                        "Charge the laser network, fire into the &eLaser Focus Matrix&r, and watch the controller for a successful ignition.",
                        "Once burning, maintain deuterium/tritium injection and cooling; pull steam/FE through your existing turbine if configured.",
                    ],
                    caution="Ignition pulls a huge power spike. If lasers brown out mid-charge, stop and reinforce the grid before retrying.",
                    tip="Craft spare Hohlraums before the first attempt — learning runs are rarely one-and-done.",
                ),
                deps=[14],
                rewards=[xp_levels(2)],
                subtitle='Mekanism Generators · Fusion',
            ),
        ],
    )
