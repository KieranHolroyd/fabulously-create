#!/usr/bin/env bash
# Build a Fabric dedicated server pack for Fabulously Create (1.20.1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
OUT_DIR="${1:-$ROOT/dist/Fabulously Create Server}"

MC_VERSION="1.20.1"
FABRIC_VERSION="0.18.6"
INSTALLER_VERSION="$(curl -fsSL https://meta.fabricmc.net/v2/versions/installer | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['version'])")"
PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"
MIN_RAM="${MIN_RAM:-2G}"
MAX_RAM="${MAX_RAM:-6G}"

echo "Building server pack → $OUT_DIR"
echo "  Minecraft $MC_VERSION · Fabric $FABRIC_VERSION"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/mods"

python3 "$ROOT/scripts/download-mods.py" "$OUT_DIR" --pack-dir "$PACK_DIR" --profile server

echo ""
echo "Downloading Fabric server launcher..."
FABRIC_URL="https://meta.fabricmc.net/v2/versions/loader/${MC_VERSION}/${FABRIC_VERSION}/${INSTALLER_VERSION}/server/jar"
curl -fsSL "$FABRIC_URL" -o "$OUT_DIR/fabric-server-launch.jar"

cat > "$OUT_DIR/eula.txt" << 'EOF'
# By changing the setting below to TRUE you are indicating your agreement to our EULA.
# https://aka.ms/MinecraftEULA
eula=false
EOF

cat > "$OUT_DIR/server.properties" << 'EOF'
motd=Fabulously Create
difficulty=normal
gamemode=survival
max-players=20
online-mode=true
pvp=true
spawn-protection=16
view-distance=10
simulation-distance=10
enable-command-block=false
EOF

cat > "$OUT_DIR/start.sh" << EOF
#!/usr/bin/env bash
set -euo pipefail
cd "\$(dirname "\$0")"

if [[ "\$(grep -E '^eula=' eula.txt | cut -d= -f2 | tr '[:upper:]' '[:lower:]')" != "true" ]]; then
  echo "Set eula=true in eula.txt before starting the server."
  exit 1
fi

JAVA="\${JAVA:-java}"
exec "\$JAVA" -Xms${MIN_RAM} -Xmx${MAX_RAM} \\
  -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \\
  -jar fabric-server-launch.jar nogui "\$@"
EOF
chmod +x "$OUT_DIR/start.sh"

cat > "$OUT_DIR/start.bat" << EOF
@echo off
cd /d "%~dp0"
findstr /B /I "eula=true" eula.txt >nul || (
  echo Set eula=true in eula.txt before starting the server.
  exit /b 1
)
java -Xms${MIN_RAM} -Xmx${MAX_RAM} -XX:+UseG1GC -jar fabric-server-launch.jar nogui %*
EOF

cat > "$OUT_DIR/README.txt" << EOF
Fabulously Create — Server Pack v${PACK_VERSION}
Minecraft ${MC_VERSION} · Fabric ${FABRIC_VERSION}

Setup:
  1. Install Java 17 or newer.
  2. Edit eula.txt — set eula=true
  3. Optional: edit server.properties and start.sh RAM settings
  4. Run ./start.sh (Linux/macOS) or start.bat (Windows)

First launch downloads Minecraft server files and generates configs.
Match this mod list with the client pack in the same repo.

Client-only mods (Sodium, Iris, JEI, Inventory Profiles, etc.) are not included.
Players install the full client pack separately via Prism Launcher.
EOF

MOD_COUNT="$(find "$OUT_DIR/mods" -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Built: $OUT_DIR"
echo "  $MOD_COUNT server mods"
echo "  Run: cd '$OUT_DIR' && edit eula.txt && ./start.sh"
