# Included mods

Based on [Fabulously Optimized](https://modrinth.com/modpack/fabulously-optimized) **1.20.1** (v5.4.x), plus Create and quality-of-life additions.

**Minecraft 1.20.1 · Fabric 0.18.6**

## Create (core + addons)

| Mod | Purpose |
| --- | --- |
| [Create Fabric](https://modrinth.com/mod/create-fabric) | Official Fabric port — kinetic engineering, contraptions, trains |
| [Create Deco](https://modrinth.com/mod/create-deco) | Industrial decorative blocks |
| [Create Crafts & Additions](https://modrinth.com/mod/createaddition) | Electricity ↔ kinetic energy bridge |
| [Create: Copycats+](https://modrinth.com/mod/copycats) | Copycat blocks for builds |
| [Create: Steam 'n' Rails](https://modrinth.com/mod/create-steam-n-rails) | Expanded rails and steam |
| [Create: New Age](https://modrinth.com/mod/create-new-age) | Electricity integration |
| [Create Big Cannons](https://modrinth.com/mod/create-big-cannons) | Buildable cannons |
| [Create: Bells & Whistles](https://modrinth.com/mod/bellsandwhistles) | Platform edges, conductors, etc. |
| [Create: Interiors](https://modrinth.com/mod/interiors) | Create-themed furniture |
| [Create Jetpack](https://modrinth.com/mod/create-jetpack) | Backtank-powered flight |
| [Create Ore Excavation](https://modrinth.com/mod/create-ore-excavation) | Vein mining with rotational force |
| [Create Goggles](https://modrinth.com/mod/create-goggles) | Goggle helmets and armored backtanks |
| [Create: Framed](https://modrinth.com/mod/create-framed) | More framed glass variants |
| [Rechiseled: Create](https://modrinth.com/mod/rechiseled-create) | Decorative Create block variants |

### Create dependencies (auto-added)

| Mod | Purpose |
| --- | --- |
| [Ritchie's Projectile Library](https://modrinth.com/mod/ritchies-projectile-lib) | Required by Create Big Cannons |
| [Architectury API](https://modrinth.com/mod/architectury-api) | Required by Create Goggles |
| [Rechiseled](https://modrinth.com/mod/rechiseled) | Required by Rechiseled: Create |

### Library dependencies (auto-added)

| Mod | Purpose |
| --- | --- |
| [SuperMartijn642's Core Lib](https://modrinth.com/mod/supermartijn642s-core-lib) | Required by Rechiseled |
| [SuperMartijn642's Config Lib](https://modrinth.com/mod/supermartijn642s-config-lib) | Required by Rechiseled |
| [Fusion (Connected Textures)](https://modrinth.com/mod/fusion-connected-textures) | Required by Rechiseled |

## Building, storage & automation

| Mod | Purpose |
| --- | --- |
| [St'ructure Tools Continued](https://modrinth.com/mod/structure-tools-continued-(building-gadget)) | Building Gadget-style copy/paste builds (Fabric) |
| [Construction Wand (Fabric)](https://modrinth.com/mod/construction-wand-fabric) | Extend blocks, fill areas, build faster |
| [Extended Drawers](https://modrinth.com/mod/extended-drawers) | Compact item storage drawers |
| [Tom's Simple Storage Mod](https://modrinth.com/mod/toms-storage) | Simple networked storage |

> **Just Dire Things** is Forge/NeoForge only on 1.20.1 — no Fabric port exists. It cannot be added without switching the whole pack off Fabric.

## Quality of life

| Mod | Purpose |
| --- | --- |
| [JourneyMap](https://modrinth.com/mod/journeymap) | In-game map and waypoints |
| [Inventory Profiles Next](https://modrinth.com/mod/inventory-profiles-next) | Inventory/chest sorting, locked slots |
| [InvTweaks Emu for IPN](https://modrinth.com/mod/invtweaks-emu-for-ipn) | Inventory Tweaks-style shortcuts |
| [Just Enough Items (JEI)](https://modrinth.com/mod/jei) | Recipe lookup |
| [libIPN](https://modrinth.com/mod/libipn) | IPN library |

## Fabulously Optimized base

Performance and visual mods from FO 1.20.1 — Sodium, Lithium, Iris, FerriteCore, Entity Culling, LambDynamicLights, Continuity, Mod Menu, Fabric API, and others. Run `packwiz list` in `pack/` for the complete set.

## Notes

- **1.20.1** is the sweet spot for Fabric Create: official port, broad addon support, stable FO base.
- **Inventory Tweaks** is replaced by **Inventory Profiles Next** + **InvTweaks Emu**.
- **Create: Design n' Decor** and **Create: Dreams & Desires** removed — incompatible with Create 6.x on Fabric.
- **JourneyMap** pinned to **5.10.3** — 6.0 beta breaks Create’s map integration mixin.
- **Controlify** removed — 2.x crashes on startup; 1.6.0 has broken controller HID on Apple Silicon. Use keyboard/mouse or wait for a fixed release.
- **Zoomify** pinned to **2.11.2** (FO original).
- Uses **Fabric Loader 0.18.6** and **Fabric API 0.92.11+** (required by Create and addons; FO's original 0.14.23 base is too old).
- For multiplayer, sync the full server mod list with clients.
- **Server pack:** run `./scripts/build-server-pack.sh` for a dedicated server without client-only mods. Players use the Prism client pack separately.

## Server vs client

| | Client (Prism) | Server |
| --- | --- | --- |
| Build | `./scripts/build-prism-instance.sh` | `./scripts/build-server-pack.sh` |
| Mods | ~82 (full FO + Create + QoL + building) | ~34 (Create + server-side FO + storage) |
| Excludes | — | Sodium, Iris, JEI, IPN, Mod Menu, … |
