#!/usr/bin/env bash
# Build the NeoForge server pack, sync it to the host in .official-server, and restart.
#
# Preserves world, logs, eula.txt, server.properties, ops/whitelist/bans, and usercache.
# Replaces mods/, libraries/, and NeoForge run scripts.
#
# Usage:
#   ./scripts/update-and-restart-server.sh
#   SKIP_BUILD=1 ./scripts/update-and-restart-server.sh   # reuse existing dist/
#   WAIT_SECS=300 ./scripts/update-and-restart-server.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
SERVER_DIR="${SERVER_DIR:-$ROOT/dist/Fabulously Create Server}"
OFFICIAL_SERVER_FILE="${OFFICIAL_SERVER_FILE:-$ROOT/.official-server}"
SERVICE="${SERVICE:-minecraft-fabric.service}"
TARGET="${TARGET:-/opt/minecraft-fabric}"
JAVA21_REMOTE="${JAVA21_REMOTE:-/usr/lib/jvm/java-21-openjdk-amd64/bin/java}"
NEOFORGE_VERSION="${NEOFORGE_VERSION:-21.1.244}"
MIN_RAM="${MIN_RAM:-2G}"
MAX_RAM="${MAX_RAM:-10G}"
WAIT_SECS="${WAIT_SECS:-300}"
SKIP_BUILD="${SKIP_BUILD:-0}"

if [[ ! -f "$OFFICIAL_SERVER_FILE" ]]; then
  echo "error: missing $OFFICIAL_SERVER_FILE (first line should be user@host)" >&2
  exit 1
fi

REMOTE="$(grep -E '^[^#[:space:]]' "$OFFICIAL_SERVER_FILE" | head -1 | tr -d '[:space:]')"
if [[ -z "$REMOTE" || "$REMOTE" != *@* ]]; then
  echo "error: could not parse user@host from $OFFICIAL_SERVER_FILE" >&2
  exit 1
fi

PACK_VERSION="$(grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/')"
STAGING="/tmp/fabulously-create-server-$$"

echo "==> Official server: $REMOTE"
echo "    Target: $TARGET  Service: $SERVICE"
echo "    Pack:   v$PACK_VERSION"

if [[ "$SKIP_BUILD" != "1" ]]; then
  echo "==> Building server pack"
  JAVA="${JAVA:-}" "$ROOT/scripts/build-server-pack.sh" "$SERVER_DIR"
else
  echo "==> Skipping build (SKIP_BUILD=1)"
  if [[ ! -d "$SERVER_DIR/mods" || ! -f "$SERVER_DIR/run.sh" ]]; then
    echo "error: incomplete server pack at $SERVER_DIR — run without SKIP_BUILD" >&2
    exit 1
  fi
fi

# Host-oriented JVM / Java path (build script defaults differ).
cat > "$SERVER_DIR/user_jvm_args.txt" << EOF
-Xms${MIN_RAM}
-Xmx${MAX_RAM}
-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
EOF

cat > "$SERVER_DIR/run.sh" << EOF
#!/usr/bin/env sh
JAVA="\${JAVA:-${JAVA21_REMOTE}}"
# Forge requires a configured set of both JVM and program arguments.
exec "\$JAVA" @user_jvm_args.txt @libraries/net/neoforged/neoforge/${NEOFORGE_VERSION}/unix_args.txt "\$@"
EOF
chmod +x "$SERVER_DIR/run.sh"
[[ -f "$SERVER_DIR/start.sh" ]] && chmod +x "$SERVER_DIR/start.sh"

MOD_COUNT="$(find "$SERVER_DIR/mods" -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
echo "==> Syncing $MOD_COUNT mods → $REMOTE:$STAGING"
ssh -o BatchMode=yes -o ConnectTimeout=15 "$REMOTE" "rm -rf '$STAGING' && mkdir -p '$STAGING'"
rsync -az --delete \
  --exclude 'world/' \
  --exclude 'world-*/' \
  --exclude 'logs/' \
  --exclude 'crash-reports/' \
  --exclude 'eula.txt' \
  --exclude 'server.properties' \
  --exclude 'ops.json' \
  --exclude 'whitelist.json' \
  --exclude 'banned-*.json' \
  --exclude 'usercache.json' \
  --exclude 'usernamecache.json' \
  --exclude '*.bak.*' \
  "$SERVER_DIR/" "$REMOTE:$STAGING/"

echo "==> Installing on host and restarting $SERVICE"
ssh -o BatchMode=yes "$REMOTE" "sudo bash -s" <<EOF
set -euo pipefail
TARGET='$TARGET'
STAGE='$STAGING'
SERVICE='$SERVICE'

sudo systemctl stop "\$SERVICE" || true

# Free the listen port if an orphan JVM is still bound.
PORT=\$(sudo grep -E '^server-port=' "\$TARGET/server.properties" 2>/dev/null | cut -d= -f2 || echo 25566)
PORT=\${PORT:-25566}
if command -v ss >/dev/null 2>&1; then
  ORPHANS=\$(sudo ss -tlnp "sport = :\$PORT" 2>/dev/null | sed -n 's/.*pid=\\([0-9]*\\).*/\\1/p' | sort -u || true)
  for pid in \$ORPHANS; do
    echo "Killing orphan listener pid \$pid on :\$PORT"
    sudo kill "\$pid" 2>/dev/null || true
  done
  sleep 1
  for pid in \$ORPHANS; do
    if sudo kill -0 "\$pid" 2>/dev/null; then
      sudo kill -9 "\$pid" 2>/dev/null || true
    fi
  done
fi

TS=\$(date +%Y%m%d-%H%M%S)
if [[ -d "\$TARGET/mods" ]]; then
  sudo cp -a "\$TARGET/mods" "\$TARGET/mods.bak.\$TS" || true
fi

sudo rm -rf "\$TARGET/mods" "\$TARGET/libraries"
sudo mkdir -p "\$TARGET/mods" "\$TARGET/config"

sudo cp -a "\$STAGE/mods/." "\$TARGET/mods/"
sudo cp -a "\$STAGE/libraries" "\$TARGET/"
sudo cp "\$STAGE/run.sh" "\$STAGE/user_jvm_args.txt" "\$TARGET/"
[[ -f "\$STAGE/start.sh" ]] && sudo cp "\$STAGE/start.sh" "\$TARGET/"
[[ -f "\$STAGE/run.bat" ]] && sudo cp "\$STAGE/run.bat" "\$TARGET/"
[[ -f "\$STAGE/start.bat" ]] && sudo cp "\$STAGE/start.bat" "\$TARGET/"
[[ -f "\$STAGE/README.txt" ]] && sudo cp "\$STAGE/README.txt" "\$TARGET/"
sudo chmod +x "\$TARGET/run.sh"
[[ -x "\$TARGET/start.sh" ]] || sudo chmod +x "\$TARGET/start.sh" 2>/dev/null || true

# Merge pack configs without wiping server-tuned files.
if [[ -d "\$STAGE/config" ]]; then
  sudo cp -a "\$STAGE/config/." "\$TARGET/config/" 2>/dev/null || true
fi
# Always replace pack-authored quest book.
if [[ -d "\$STAGE/config/ftbquests" ]]; then
  sudo rm -rf "\$TARGET/config/ftbquests"
  sudo cp -a "\$STAGE/config/ftbquests" "\$TARGET/config/ftbquests"
fi

# Datapacks: sync pack-provided packs; drop retired pack datapacks.
if [[ -d "\$STAGE/datapacks" ]]; then
  sudo mkdir -p "\$TARGET/datapacks"
  sudo cp -a "\$STAGE/datapacks/." "\$TARGET/datapacks/"
else
  sudo rm -rf "\$TARGET/datapacks/fabulously-create-ore-veins"
fi
# Keep eula accepted; ensure port stays on the modded slot if properties exist.
echo 'eula=true' | sudo tee "\$TARGET/eula.txt" >/dev/null
if [[ -f "\$TARGET/server.properties" ]]; then
  if ! grep -qE '^server-port=' "\$TARGET/server.properties"; then
    echo 'server-port=25566' | sudo tee -a "\$TARGET/server.properties" >/dev/null
  fi
fi

sudo chown -R minecraft:minecraft "\$TARGET"
sudo systemctl reset-failed "\$SERVICE" 2>/dev/null || true
sudo systemctl start "\$SERVICE"
rm -rf "\$STAGE"

echo "mods: \$(find "\$TARGET/mods" -name '*.jar' | wc -l | tr -d ' ')"
sudo systemctl is-active "\$SERVICE"
EOF

echo "==> Waiting for boot (up to ${WAIT_SECS}s)..."
# Anchor to this invocation so we don't match a previous run's "Done (" line.
BOOT_SINCE="$(ssh -o BatchMode=yes "$REMOTE" "date -u '+%Y-%m-%d %H:%M:%S UTC'")"
deadline=$((SECONDS + WAIT_SECS))
while (( SECONDS < deadline )); do
  if ssh -o BatchMode=yes "$REMOTE" \
    "sudo journalctl -u '$SERVICE' --since '$BOOT_SINCE' --no-pager 2>/dev/null | grep -qE 'Done \\(|For help, type'"; then
    echo "==> Server ready"
    ssh -o BatchMode=yes "$REMOTE" \
      "sudo systemctl status '$SERVICE' --no-pager | head -14; echo '---'; sudo grep -E '^server-port=|^motd=' '$TARGET/server.properties' || true; echo '---'; sudo ls '$TARGET/mods' | grep -iE 'leaf|rapid' || true"
    exit 0
  fi
  if ! ssh -o BatchMode=yes "$REMOTE" "systemctl is-active --quiet '$SERVICE'"; then
    echo "error: $SERVICE is not active" >&2
    ssh -o BatchMode=yes "$REMOTE" "sudo journalctl -u '$SERVICE' --since '$BOOT_SINCE' -n 80 --no-pager" || true
    exit 1
  fi
  sleep 5
done

echo "error: timed out waiting for Done (" >&2
ssh -o BatchMode=yes "$REMOTE" "sudo journalctl -u '$SERVICE' --since '$BOOT_SINCE' -n 80 --no-pager" || true
exit 1
