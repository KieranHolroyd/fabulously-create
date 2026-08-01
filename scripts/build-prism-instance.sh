#!/usr/bin/env bash
# Build a Prism Launcher / MultiMC instance folder for Fabulously Create (NeoForge 1.21.1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
OUT_DIR="${1:-$ROOT/dist/Fabulously Create}"
INSTALL="${INSTALL:-0}"

detect_prism_instances() {
  local candidate
  local -a candidates=()

  case "$(uname -s)" in
    Darwin)
      candidates+=("$HOME/Library/Application Support/PrismLauncher/instances")
      ;;
    Linux)
      candidates+=(
        "${XDG_DATA_HOME:-$HOME/.local/share}/PrismLauncher/instances"
        "$HOME/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances"
        "$HOME/.local/share/PrismLauncher/instances"
      )
      # Git Bash/MSYS and WSL can expose the Windows Prism data directory.
      if [[ -n "${APPDATA:-}" ]]; then
        candidates+=("$APPDATA/PrismLauncher/instances")
      fi
      ;;
    MINGW*|MSYS*|CYGWIN*)
      candidates+=("${APPDATA:-$HOME/AppData/Roaming}/PrismLauncher/instances")
      ;;
  esac

  # Prefer an existing Prism installation, especially one already containing
  # this pack. This also selects Flatpak Prism when that is what is installed.
  for candidate in "${candidates[@]}"; do
    if [[ -d "$candidate/Fabulously Create" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  for candidate in "${candidates[@]}"; do
    if [[ -d "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done

  # Nothing exists yet: use the native platform's standard location.
  if (( ${#candidates[@]} )); then
    printf '%s\n' "${candidates[0]}"
  else
    echo "Unable to determine the Prism instances directory." >&2
    echo "Set PRISM_INSTANCES=/path/to/PrismLauncher/instances and retry." >&2
    return 1
  fi
}

PRISM_INSTANCES="${PRISM_INSTANCES:-}"
if [[ "$INSTALL" == "1" && -z "$PRISM_INSTANCES" ]]; then
  PRISM_INSTANCES="$(detect_prism_instances)"
fi

MC_VERSION="1.21.1"
NEOFORGE_VERSION="21.1.244"
LWJGL_VERSION="3.3.3"
PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"
# Use Prism's Java 21 runtime when present, otherwise the Java on PATH.
PRISM_ROOT="${PRISM_ROOT:-${PRISM_INSTANCES%/instances}}"
PRISM_JAVA_DELTA="${PRISM_JAVA_DELTA:-$PRISM_ROOT/java/java-runtime-delta/bin/java}"
if [[ -z "${JAVA_PATH:-}" ]]; then
  if [[ -x "$PRISM_JAVA_DELTA" ]]; then
    JAVA_PATH="$PRISM_JAVA_DELTA"
  else
    JAVA_PATH="$(command -v java || true)"
  fi
fi
JAVA_ARCH="$(uname -m)"
[[ "$JAVA_ARCH" == "x86_64" ]] && JAVA_ARCH="amd64"
[[ "$JAVA_ARCH" == "arm64" ]] && JAVA_ARCH="aarch64"
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
JavaRealArchitecture=$JAVA_ARCH
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

# Avoid Create 6.0.10 chocolate_bucket advancement boot crash on large packs.
CREATE_JAR="$(find "$OUT_DIR/minecraft/mods" -maxdepth 1 -name 'create-1.21.1-*.jar' | head -n 1 || true)"
if [[ -n "$CREATE_JAR" ]]; then
  echo "Patching Create bootfix → $CREATE_JAR"
  python3 "$ROOT/scripts/patch-create-bootfix.py" "$CREATE_JAR" "$CREATE_JAR.patched"
  mv "$CREATE_JAR.patched" "$CREATE_JAR"
fi

MOD_COUNT="$(find "$OUT_DIR/minecraft/mods" -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Built: $OUT_DIR ($MOD_COUNT mods)"

if [[ "$INSTALL" == "1" ]]; then
  DEST="$PRISM_INSTANCES/Fabulously Create"
  echo "Installing to $DEST ..."

  if [[ ! -d "$DEST" ]]; then
    mkdir -p "$PRISM_INSTANCES"
    cp -R "$OUT_DIR" "$DEST"
    echo "Done. Fresh instance installed. Open Prism Launcher and launch 'Fabulously Create' (Java 21)."
  else
    echo "Updating existing instance (preserving settings, configs, worlds, servers)..."

    # Loader / instance metadata
    cp "$OUT_DIR/mmc-pack.json" "$DEST/mmc-pack.json"

    # Keep user Prism settings (RAM, window, JVM args, etc.); refresh Java + pack notes.
    if [[ -f "$DEST/instance.cfg" ]]; then
      python3 - "$DEST/instance.cfg" "$OUT_DIR/instance.cfg" <<'PY'
import sys
from pathlib import Path

dest_path = Path(sys.argv[1])
fresh_path = Path(sys.argv[2])

def parse(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data

old = parse(dest_path)
fresh = parse(fresh_path)
# Pack-owned keys we always refresh from the build.
for key in (
    "InstanceType",
    "iconKey",
    "name",
    "notes",
    "AutomaticJava",
    "OverrideJavaLocation",
    "JavaPath",
    "JavaSignature",
    "JavaVersion",
    "JavaVendor",
    "JavaArchitecture",
    "JavaRealArchitecture",
    "IgnoreJavaCompatibility",
):
    if key in fresh:
        old[key] = fresh[key]

lines = [f"{k}={v}" for k, v in old.items()]
dest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
    else
      cp "$OUT_DIR/instance.cfg" "$DEST/instance.cfg"
    fi

    # Replace mod jars only (drop removed mods, add new ones).
    mkdir -p "$DEST/minecraft"
    rm -rf "$DEST/minecraft/mods"
    cp -R "$OUT_DIR/minecraft/mods" "$DEST/minecraft/mods"

    # Pack resourcepacks: update/add without deleting user-installed packs.
    if [[ -d "$OUT_DIR/minecraft/resourcepacks" ]]; then
      mkdir -p "$DEST/minecraft/resourcepacks"
      cp -R "$OUT_DIR/minecraft/resourcepacks/." "$DEST/minecraft/resourcepacks/"
    fi

    # Pack datapacks: update/add without deleting user-installed packs.
    if [[ -d "$OUT_DIR/minecraft/datapacks" ]]; then
      mkdir -p "$DEST/minecraft/datapacks"
      cp -R "$OUT_DIR/minecraft/datapacks/." "$DEST/minecraft/datapacks/"
    fi
    # Drop retired pack datapacks / ore-vein overrides so mod defaults apply.
    rm -rf "$DEST/minecraft/datapacks/fabulously-create-ore-veins"
    rm -f "$DEST/minecraft/config/largeoreveins-common.toml"
    rm -f "$DEST/minecraft/mods"/globalpacks-*.jar

    # Pack configs: only fill in missing files; never overwrite user-tuned settings.
    if [[ -d "$OUT_DIR/minecraft/config" ]]; then
      mkdir -p "$DEST/minecraft/config"
      if command -v rsync >/dev/null 2>&1; then
        rsync -a --ignore-existing "$OUT_DIR/minecraft/config/" "$DEST/minecraft/config/"
      else
        (
          cd "$OUT_DIR/minecraft/config"
          find . -type f | while IFS= read -r rel; do
            rel="${rel#./}"
            if [[ ! -e "$DEST/minecraft/config/$rel" ]]; then
              mkdir -p "$DEST/minecraft/config/$(dirname "$rel")"
              cp "$OUT_DIR/minecraft/config/$rel" "$DEST/minecraft/config/$rel"
            fi
          done
        )
      fi
    fi

    # Always refresh pack-authored FTB Quests (overwrite local quest book).
    if [[ -d "$OUT_DIR/minecraft/config/ftbquests" ]]; then
      rm -rf "$DEST/minecraft/config/ftbquests"
      mkdir -p "$DEST/minecraft/config"
      cp -R "$OUT_DIR/minecraft/config/ftbquests" "$DEST/minecraft/config/ftbquests"
    fi

    echo "Done. Preserved options/config/saves/servers; refreshed mods + loader metadata."
    echo "Open Prism Launcher and launch 'Fabulously Create' (Java 21)."
  fi
else
  echo ""
  echo "To install into Prism Launcher:"
  echo "  INSTALL=1 $0"
  echo ""
  echo "Or copy manually:"
  echo "  cp -R '$OUT_DIR' '<your PrismLauncher instances folder>/'"
fi
