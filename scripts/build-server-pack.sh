#!/usr/bin/env bash
# Build a NeoForge dedicated server pack for Fabulously Create (1.21.1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
OUT_DIR="${1:-$ROOT/dist/Fabulously Create Server}"

MC_VERSION="1.21.1"
NEOFORGE_VERSION="21.1.244"
PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"
MIN_RAM="${MIN_RAM:-2G}"
MAX_RAM="${MAX_RAM:-6G}"

# Prefer JAVA_HOME / JAVA, then common macOS / Homebrew / Prism runtimes.
resolve_java() {
  if [[ -n "${JAVA:-}" && -x "${JAVA}" ]]; then
    echo "$JAVA"
    return
  fi
  if [[ -n "${JAVA_HOME:-}" && -x "${JAVA_HOME}/bin/java" ]]; then
    echo "${JAVA_HOME}/bin/java"
    return
  fi
  for candidate in \
    "/opt/homebrew/opt/openjdk@21/bin/java" \
    "/opt/homebrew/opt/openjdk/bin/java" \
    "/usr/local/opt/openjdk@21/bin/java" \
    "$HOME/Library/Application Support/PrismLauncher/java/java-runtime-delta/jre.bundle/Contents/Home/bin/java" \
    "$HOME/Library/Application Support/PrismLauncher/java/java-runtime-epsilon/jre.bundle/Contents/Home/bin/java" \
    "$(command -v java 2>/dev/null || true)"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
      echo "$candidate"
      return
    fi
  done
  echo "error: Java 21+ required to install NeoForge server (set JAVA=...)" >&2
  exit 1
}

JAVA_BIN="$(resolve_java)"

echo "Building server pack → $OUT_DIR"
echo "  Minecraft $MC_VERSION · NeoForge $NEOFORGE_VERSION"
echo "  Java: $JAVA_BIN"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/mods"

python3 "$ROOT/scripts/download-mods.py" "$OUT_DIR" --pack-dir "$PACK_DIR" --profile server

echo ""
echo "Downloading NeoForge installer..."
INSTALLER_JAR="$OUT_DIR/neoforge-${NEOFORGE_VERSION}-installer.jar"
INSTALLER_URL="https://maven.neoforged.net/releases/net/neoforged/neoforge/${NEOFORGE_VERSION}/neoforge-${NEOFORGE_VERSION}-installer.jar"
curl -fsSL "$INSTALLER_URL" -o "$INSTALLER_JAR"

echo "Running NeoForge server installer..."
install_ok=0
for attempt in 1 2 3; do
  if (
    cd "$OUT_DIR"
    "$JAVA_BIN" -jar "$INSTALLER_JAR" --installServer
  ); then
    install_ok=1
    break
  fi
  echo "NeoForge installer attempt $attempt failed; retrying..." >&2
  sleep 2
done
if [[ "$install_ok" != "1" ]]; then
  echo "error: NeoForge server installer failed after retries" >&2
  exit 1
fi
rm -f "$INSTALLER_JAR" "$OUT_DIR"/neoforge-*-installer.jar.log "$OUT_DIR/installer.log" 2>/dev/null || true

# Prefer installer-generated run scripts; wrap with RAM defaults if present.
if [[ -f "$OUT_DIR/user_jvm_args.txt" ]]; then
  cat > "$OUT_DIR/user_jvm_args.txt" << EOF
-Xms${MIN_RAM}
-Xmx${MAX_RAM}
-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
EOF
fi

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

cat > "$OUT_DIR/start.sh" << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ "$(grep -E '^eula=' eula.txt | cut -d= -f2 | tr '[:upper:]' '[:lower:]')" != "true" ]]; then
  echo "Set eula=true in eula.txt before starting the server."
  exit 1
fi

if [[ -x ./run.sh ]]; then
  exec ./run.sh nogui "$@"
fi

echo "error: NeoForge run.sh missing — re-run scripts/build-server-pack.sh" >&2
exit 1
EOF
chmod +x "$OUT_DIR/start.sh"
[[ -f "$OUT_DIR/run.sh" ]] && chmod +x "$OUT_DIR/run.sh"

cat > "$OUT_DIR/start.bat" << 'EOF'
@echo off
cd /d "%~dp0"
findstr /B /I "eula=true" eula.txt >nul || (
  echo Set eula=true in eula.txt before starting the server.
  exit /b 1
)
if exist run.bat (
  call run.bat nogui %*
) else (
  echo error: NeoForge run.bat missing — re-run scripts\build-server-pack.sh
  exit /b 1
)
EOF

cat > "$OUT_DIR/README.txt" << EOF
Fabulously Create — Server Pack v${PACK_VERSION}
Minecraft ${MC_VERSION} · NeoForge ${NEOFORGE_VERSION}

Setup:
  1. Install Java 21 or newer.
  2. Edit eula.txt — set eula=true
  3. Optional: edit server.properties and user_jvm_args.txt RAM settings
  4. Run ./start.sh (Linux/macOS) or start.bat (Windows)

First launch generates mod configs.
Match this mod list with the client pack in the same repo.

Client-only mods (Sodium, Iris, JEI, Mouse Tweaks, Just Zoom, etc.) are not included.
Players install the full client pack separately via Prism Launcher.
EOF

MOD_COUNT="$(find "$OUT_DIR/mods" -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Built: $OUT_DIR"
echo "  $MOD_COUNT server mods"
echo "  Run: cd '$OUT_DIR' && edit eula.txt && ./start.sh"
