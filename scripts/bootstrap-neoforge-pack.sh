#!/usr/bin/env bash
# Rebuild the NeoForge 1.21.1 mod manifest from a curated list.
# Clears pack/mods and re-adds via packwiz (Modrinth + CurseForge).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
PACKWIZ="${PACKWIZ:-$(command -v packwiz || echo "$HOME/go/bin/packwiz")}"

if [[ ! -x "$PACKWIZ" && ! -f "$PACKWIZ" ]]; then
  echo "packwiz not found. Install with: go install github.com/packwiz/packwiz@latest" >&2
  exit 1
fi

cd "$PACK_DIR"

echo "Clearing pack/mods..."
rm -f mods/*.pw.toml
mkdir -p mods

add_mr() {
  local slug="$1"
  echo "==> Modrinth: $slug"
  "$PACKWIZ" -y modrinth add "$slug" || {
    echo "WARNING: failed to add $slug" >&2
    return 0
  }
}

add_cf_url() {
  local url="$1"
  echo "==> CurseForge: $url"
  "$PACKWIZ" -y curseforge add "$url" || {
    echo "WARNING: failed to add $url" >&2
    return 0
  }
}

echo "Adding performance stack..."
add_mr sodium
add_mr iris
add_mr modernfix
add_mr ferrite-core
add_mr kotlin-for-forge

echo "Adding Create + addons..."
add_mr create
add_mr create-deco
add_mr createaddition
add_mr copycats
add_mr create-big-cannons
add_mr create-new-age
add_mr create-jetpack
add_mr interiors
add_mr bellsandwhistles
add_mr create-ore-excavation
add_mr create-steam-n-rails-1.21.1
add_mr slice-and-dice
add_mr create-connected
add_mr create-dragons-plus
add_mr create-enchantment-industry
add_mr create-diesel-generators
add_mr create-stuff-additions

echo "Adding storage..."
add_mr sophisticated-core
add_mr sophisticated-backpacks
add_mr sophisticated-storage
add_mr functional-storage
add_mr toms-storage
add_mr pipez
add_mr iron-chests

echo "Adding Integrated Dynamics stack..."
add_mr cyclops-core
add_mr common-capabilities
add_mr integrated-dynamics
add_mr integrated-tunnels
add_mr integrated-terminals
add_mr integrated-crafting

echo "Adding Silent Gear..."
add_mr silent-lib
add_mr silent-gear

echo "Adding Iron Jetpacks..."
add_mr cucumber
add_mr iron-jetpacks

echo "Adding curios / artifacts..."
add_mr curios
add_mr artifacts

echo "Adding building tools..."
add_mr construction-sticks
add_mr crafting-on-a-stick
add_mr supplementaries
add_mr another-furniture
add_cf_url "https://www.curseforge.com/minecraft/mc-mods/building-gadgets/files/6850515"

echo "Adding world generation..."
add_mr large-ore-veins

echo "Adding QoL..."
add_mr jei
add_mr journeymap
add_mr jade
add_mr appleskin
add_mr balm
add_mr trashslot
add_mr inventory-essentials
add_mr waystones
add_mr natures-compass
add_mr explorers-compass
add_mr lootr
add_mr comforts
add_mr mouse-tweaks
add_mr controlling
add_mr just-zoom
add_mr rapid-leaf-decay
add_mr cloth-config
add_mr architectury-api
add_mr entityculling
add_mr immediatelyfast

echo "Adding FTB Ultimine + Corail Tombstone (CurseForge NeoForge)..."
add_cf_url "https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge/files/8231400"
add_cf_url "https://www.curseforge.com/minecraft/mc-mods/corail-tombstone/files/8425866"

"$PACKWIZ" refresh

echo ""
echo "Bootstrap complete. Mods:"
ls mods/*.pw.toml | wc -l | tr -d ' '
"$PACKWIZ" list 2>/dev/null | head -80 || true
