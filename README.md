# Fabulously Create

A Minecraft **Fabric 1.20.1** modpack built on [Fabulously Optimized](https://modrinth.com/modpack/fabulously-optimized) — keeping its performance and visual polish — with the **official [Create Fabric](https://modrinth.com/mod/create-fabric)** port, a wide set of Create addons, **JourneyMap**, **Inventory Sorting**, and **JEI**.

## Quick install (Prism Launcher)

**Minecraft 1.20.1 · Fabric 0.18.6**

```bash
./scripts/build-prism-instance.sh
INSTALL=1 ./scripts/build-prism-instance.sh
```

The first command writes `dist/Fabulously Create/`. The second copies it into Prism's instances folder (macOS: `~/Library/Application Support/PrismLauncher/instances/`).

Open Prism Launcher and launch **Fabulously Create**. Prism downloads Minecraft and Fabric on first launch.

## Dedicated server

Build a server pack (client-only mods stripped — Sodium, Iris, JEI, Inventory Sorting, etc.):

```bash
./scripts/build-server-pack.sh
```

Output: `dist/Fabulously Create Server/`

```bash
cd "dist/Fabulously Create Server"
# Edit eula.txt → eula=true
./start.sh
```

First launch downloads the vanilla server jar and generates mod configs. **All players** still need the full **client** pack from `./scripts/build-prism-instance.sh`.

Server includes all Create mods + server-side FO mods (Lithium, FerriteCore, ModernFix, JourneyMap server, …). See `scripts/server-mod-denylist.txt` for excluded client mods.

### Fixing "Fabulously Optimized again" error

FO's YOSBR mod restores a trap config if `config/fabric_loader_dependencies.json` is missing. This pack replaces that with Fabulously Create configs. If you still see the error on an existing instance, replace `minecraft/config/fabric_loader_dependencies.json` with the one from a fresh build, or run `INSTALL=1 ./scripts/build-prism-instance.sh` for a clean install.

## What's included

See [INCLUDED-MODS.md](INCLUDED-MODS.md) for the full list.

**Highlights:**

- Full Fabulously Optimized stack (Sodium, Lithium, Iris, …)
- **Create Fabric** + 15 Create addons (Deco, Copycats+, Steam 'n' Rails, Big Cannons, …)
- St'ructure Tools Continued (Building Gadget), Construction Wand, Extended Drawers, Tom's Storage, Functional Storage
- JourneyMap
- Inventory Sorting
- FTB Ultimine (vein mining)
- Sophisticated Backpacks
- JEI

> **Just Dire Things** isn't available on Fabric 1.20.1 (Forge/NeoForge only).

## Releases

Bump `version` in `pack/pack.toml`, commit, then create a GitHub release with tag `vX.Y.Z` matching that version (e.g. `v1.0.5`). CI builds and uploads:

- `Fabulously-Create-X.Y.Z.mrpack` — Modrinth / launcher client pack
- `Fabulously-Create-Server-X.Y.Z.zip` — dedicated server pack
- `Fabulously-Create-Prism-X.Y.Z.zip` — Prism Launcher instance folder

Build locally:

```bash
./scripts/build-release.sh
```

**Modrinth auto-upload (optional):** In repo **Settings → Secrets and variables → Actions**, add secret `MODRINTH_TOKEN` (Modrinth PAT with *Create versions* scope) and variable `MODRINTH_PROJECT_ID` (your Modrinth project ID). Without the variable, CI still attaches files to GitHub Releases only.

You can also trigger a test build from **Actions → Release → Run workflow**; artifacts are kept for 14 days.

## Developing / updating the pack

Requires [packwiz](https://github.com/packwiz/packwiz):

```bash
go install github.com/packwiz/packwiz@latest
cd pack
packwiz list
packwiz modrinth add <slug>
packwiz update --all && packwiz refresh
```

```bash
./scripts/add-mod.sh <modrinth-slug>
./scripts/build-prism-instance.sh
```

## Multiplayer

- **Create Fabric** and all Create addons must be on both client and server.
- JourneyMap and Inventory Sorting are client-side optional.
- Match the full mod list on the server for best compatibility.

## Credits

- [Fabulously Optimized](https://github.com/Fabulously-Optimized/fabulously-optimized) — base modpack
- [Create Fabric](https://modrinth.com/mod/create-fabric) — Fabricators of Create
- All mod authors in [INCLUDED-MODS.md](INCLUDED-MODS.md)

## License

Modpack metadata and scripts are provided as-is. Individual mods retain their own licenses.
