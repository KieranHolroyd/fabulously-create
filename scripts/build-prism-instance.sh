#!/usr/bin/env bash
# Build a Prism Launcher / MultiMC instance folder for Fabulously Create (1.20.1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
OUT_DIR="${1:-$ROOT/dist/Fabulously Create}"
PRISM_INSTANCES="${PRISM_INSTANCES:-$HOME/Library/Application Support/PrismLauncher/instances}"
INSTALL="${INSTALL:-0}"

MC_VERSION="1.20.1"
FABRIC_VERSION="0.18.6"
LWJGL_VERSION="3.3.1"
PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"

echo "Building Prism instance → $OUT_DIR"
echo "  Minecraft $MC_VERSION · Fabric $FABRIC_VERSION"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/minecraft"

cat > "$OUT_DIR/instance.cfg" << EOF
InstanceType=OneSix
iconKey=pack
name=Fabulously Create
notes=Fabulously Optimized + Create (Fabric) and addons. MC $MC_VERSION Fabric $FABRIC_VERSION. Pack v$PACK_VERSION.
EOF

cat > "$OUT_DIR/mmc-pack.json" << EOF
{
  "components": [
    {
      "cachedName": "Minecraft",
      "cachedRequires": [
        {
          "suggests": "$LWJGL_VERSION",
          "uid": "org.lwjgl3"
        }
      ],
      "cachedVersion": "$MC_VERSION",
      "important": true,
      "uid": "net.minecraft",
      "version": "$MC_VERSION"
    },
    {
      "cachedName": "LWJGL 3",
      "cachedVersion": "$LWJGL_VERSION",
      "cachedVolatile": true,
      "dependencyOnly": true,
      "uid": "org.lwjgl3",
      "version": "$LWJGL_VERSION"
    },
    {
      "cachedName": "Intermediary Mappings",
      "cachedRequires": [
        {
          "equals": "$MC_VERSION",
          "uid": "net.minecraft"
        }
      ],
      "cachedVersion": "$MC_VERSION",
      "cachedVolatile": true,
      "dependencyOnly": true,
      "uid": "net.fabricmc.intermediary",
      "version": "$MC_VERSION"
    },
    {
      "cachedName": "Fabric Loader",
      "cachedRequires": [
        {
          "uid": "net.fabricmc.intermediary"
        }
      ],
      "cachedVersion": "$FABRIC_VERSION",
      "uid": "net.fabricmc.fabric-loader",
      "version": "$FABRIC_VERSION"
    }
  ],
  "formatVersion": 1
}
EOF

python3 "$ROOT/scripts/download-mods.py" "$OUT_DIR/minecraft" --pack-dir "$PACK_DIR" --profile full

MOD_COUNT="$(find "$OUT_DIR/minecraft/mods" -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Built: $OUT_DIR ($MOD_COUNT mods)"

if [[ "$INSTALL" == "1" ]]; then
  DEST="$PRISM_INSTANCES/Fabulously Create"
  echo "Installing to $DEST ..."
  rm -rf "$DEST"
  cp -R "$OUT_DIR" "$DEST"
  echo "Done. Open Prism Launcher and launch 'Fabulously Create'."
else
  echo ""
  echo "To install into Prism Launcher:"
  echo "  INSTALL=1 $0"
  echo ""
  echo "Or copy manually:"
  echo "  cp -R '$OUT_DIR' '$PRISM_INSTANCES/'"
fi
