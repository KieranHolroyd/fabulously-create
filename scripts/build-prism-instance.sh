#!/usr/bin/env bash
# Build a Prism Launcher / MultiMC instance folder for Fabulously Create (NeoForge 1.21.1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
OUT_DIR="${1:-$ROOT/dist/Fabulously Create}"
PRISM_INSTANCES="${PRISM_INSTANCES:-$HOME/Library/Application Support/PrismLauncher/instances}"
INSTALL="${INSTALL:-0}"

MC_VERSION="1.21.1"
NEOFORGE_VERSION="21.1.244"
LWJGL_VERSION="3.3.3"
PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"
# Prism ships java-runtime-delta as Java 21 on macOS; override via JAVA_PATH if needed.
PRISM_ROOT="${PRISM_ROOT:-$HOME/Library/Application Support/PrismLauncher}"
PRISM_JAVA_DELTA="${PRISM_JAVA_DELTA:-$PRISM_ROOT/java/java-runtime-delta/bin/java}"
JAVA_PATH="${JAVA_PATH:-$PRISM_JAVA_DELTA}"
# Match Prism's stored metadata for java-runtime-delta (avoids auto-switch back to Java 17).
JAVA_SIGNATURE="${JAVA_SIGNATURE:-fa5f76517923fd49498ea181ba6e2aa62643a065}"
JAVA_VERSION_STR="${JAVA_VERSION_STR:-21.0.7}"

echo "Building Prism instance → $OUT_DIR"
echo "  Minecraft $MC_VERSION · NeoForge $NEOFORGE_VERSION"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/minecraft"

cat > "$OUT_DIR/instance.cfg" << EOF
InstanceType=OneSix
iconKey=pack
name=Fabulously Create
notes=Create + Silent Gear + Sophisticated Storage on NeoForge. MC $MC_VERSION NeoForge $NEOFORGE_VERSION. Pack v$PACK_VERSION. Requires Java 21.
AutomaticJava=false
OverrideJavaLocation=true
JavaPath=$JAVA_PATH
JavaSignature=$JAVA_SIGNATURE
JavaVersion=$JAVA_VERSION_STR
JavaVendor=Microsoft
JavaArchitecture=64
JavaRealArchitecture=aarch64
IgnoreJavaCompatibility=false
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
      "cachedName": "NeoForge",
      "cachedRequires": [
        {
          "uid": "net.minecraft",
          "equals": "$MC_VERSION"
        }
      ],
      "cachedVersion": "$NEOFORGE_VERSION",
      "uid": "net.neoforged",
      "version": "$NEOFORGE_VERSION"
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
  echo "Done. Open Prism Launcher and launch 'Fabulously Create' (Java 21)."
else
  echo ""
  echo "To install into Prism Launcher:"
  echo "  INSTALL=1 $0"
  echo ""
  echo "Or copy manually:"
  echo "  cp -R '$OUT_DIR' '$PRISM_INSTANCES/'"
fi
