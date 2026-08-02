# Fabulously Create

A Minecraft **NeoForge 1.21.1** modpack focused on **Create**, **Silent Gear**, **Sophisticated Backpacks/Storage**, and **Functional Storage**, with **Sodium + Iris** (beta), ModernFix, and FerriteCore.

> **v2.0.0** migrated from Fabric 1.20.1. Worlds and configs from the Fabric pack are not compatible.

## Quick install (Prism Launcher)

**Minecraft 1.21.1 · NeoForge 21.1.244 · Java 21+**

```bash
./scripts/build-prism-instance.sh
INSTALL=1 ./scripts/build-prism-instance.sh
```

The first command writes `dist/Fabulously Create/`. The second locates Prism's instances folder on macOS, Linux, Flatpak Linux, or Windows (Git Bash/MSYS). Set `PRISM_INSTANCES=/custom/path/instances` if Prism uses a custom location.

`INSTALL=1` on an existing instance updates mods and loader metadata only — it keeps `options.txt`, `config/`, worlds, servers, resource packs, and Prism RAM/JVM settings.

Open Prism Launcher and launch **Fabulously Create**. Use a **Java 21** runtime in instance settings if Prism does not pick one automatically.

## Dedicated server

Build a server pack (client-only mods stripped — Sodium, Iris, Mouse Tweaks, Just Zoom, Controlling, etc.):

```bash
./scripts/build-server-pack.sh
```

Output: `dist/Fabulously Create Server/`

```bash
cd "dist/Fabulously Create Server"
# Edit eula.txt → eula=true
./start.sh
```

Requires **Java 21+**. First launch generates mod configs. **All players** still need the full **client** pack from `./scripts/build-prism-instance.sh`.

See `scripts/server-mod-denylist.txt` for excluded client mods.

### Official host (update + restart)

Put `user@host` on the first line of `.official-server` (gitignored), then:

```bash
./scripts/update-and-restart-server.sh
```

Rebuilds the server pack, rsyncs mods/libraries/run scripts to `/opt/minecraft-fabric`, restarts `minecraft-fabric.service`, and waits for boot. World, `server.properties`, and player data are preserved. Use `SKIP_BUILD=1` to redeploy an existing `dist/Fabulously Create Server/`.

## What's included

See [INCLUDED-MODS.md](INCLUDED-MODS.md) for the full list.

**Highlights:**

- **Create** + addons (Aeronautics, Slice & Dice, Connected, Enchantment Industry, Diesel Generators, Stuff 'N Additions, Steam 'n' Rails beta, …)
- **Farmer's Delight** + Create food automation
- **Integrated Dynamics** + Tunnels / Terminals / Crafting
- **Powah** generators, energy storage, cables, reactors, and wireless charging
- **RFTools** power, automation, storage scanning, teleportation, and custom dimensions
- **Flux Networks** cross-dimensional wireless FE transfer and storage
- **Silent Gear**, **Iron Jetpacks**, **Curios**, **Artifacts**
- **Refined Storage** item/fluid networks + Extra Disks, ExtraStorage, JEI and Curios integration
- **Sophisticated** storage/backpacks, Functional Storage, Tom's, Pipez, Iron Chests, Iron Furnaces
- **Waystones**, Lootr, Comforts, Supplementaries, Another Furniture
- **FTB Ultimine**, **FTB Quests** (212 quests across 9 chapters, including dedicated Refined Storage, Powah, RFTools, and Flux Networks categories), Large Ore Veins, Corail Tombstone
- Sodium, Iris (beta), Entity Culling, ImmediatelyFast, ModernFix, FerriteCore
- JourneyMap, Jade, JEI + ore-height distribution, AppleSkin, TrashSlot, Inventory Essentials

**Dropped / replaced vs Fabric FO pack:**

- Most FO visual QoL (YOSBR, Continuity, LambDynamicLights, …) — not FO parity
- Zoomify → Just Zoom; Construction Wand → Construction Sticks
- Extended Drawers (use Functional Storage)

## Releases

Bump `version` in `pack/pack.toml`, commit, then either:

- Push a tag: `git tag v2.0.0 && git push origin v2.0.0` — CI builds and creates/updates the GitHub Release, or
- Create a GitHub Release in the UI with tag `vX.Y.Z` matching `pack.toml`

CI always uploads to **GitHub Releases**:

- `Fabulously-Create-X.Y.Z.mrpack` — Modrinth / launcher client pack
- `Fabulously-Create-Server-X.Y.Z.zip` — dedicated server pack
- `Fabulously-Create-Prism-X.Y.Z.zip` — Prism Launcher instance folder

Build locally:

```bash
./scripts/build-release.sh
```

**Modrinth auto-upload (optional):** Add secret `MODRINTH_TOKEN` and variable `MODRINTH_PROJECT_ID` in repo **Settings → Secrets and variables → Actions**. If either is missing, CI skips Modrinth and still publishes to GitHub Releases.

You can also run **Actions → Release → Run workflow** to build from `pack.toml` and publish a GitHub Release without Modrinth.

## Developing / updating the pack

Requires [packwiz](https://github.com/packwiz/packwiz):

```bash
go install github.com/packwiz/packwiz@latest
cd pack
packwiz list
packwiz modrinth add <slug>
packwiz update --all && packwiz refresh
```

Rebuild the curated NeoForge list from scratch:

```bash
./scripts/bootstrap-neoforge-pack.sh
./scripts/build-prism-instance.sh
```

```bash
./scripts/add-mod.sh <modrinth-slug>
./scripts/build-prism-instance.sh
```

## Multiplayer

- Create and all Create addons must be on both client and server.
- Silent Gear, Sophisticated mods, and Functional Storage must match on both sides.
- Mouse Tweaks / Just Zoom / Controlling are client-only (excluded from the server pack). JEI, Jade, and JourneyMap are included on the server.

## Credits

- [Create](https://modrinth.com/mod/create) and addon authors
- [Silent Gear](https://modrinth.com/mod/silent-gear) — SilentChaos512
- [Sophisticated Backpacks / Storage](https://modrinth.com/mod/sophisticated-backpacks) — P3pp3rF1y
- All mod authors in [INCLUDED-MODS.md](INCLUDED-MODS.md)

## License

Modpack metadata and scripts are provided as-is. Individual mods retain their own licenses.
