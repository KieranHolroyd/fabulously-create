#!/usr/bin/env bash
# Build all release artifacts for Fabulously Create.
#
# Outputs to dist/release/:
#   Fabulously-Create-<version>.mrpack       — Modrinth / launcher client pack
#   Fabulously-Create-Server-<version>.zip   — dedicated server pack
#   Fabulously-Create-Prism-<version>.zip    — Prism Launcher instance folder
#
# Usage:
#   ./scripts/build-release.sh
#   EXPECTED_VERSION=1.0.5 ./scripts/build-release.sh   # fail if pack.toml differs
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
RELEASE_DIR="$ROOT/dist/release"
SERVER_DIR="$ROOT/dist/Fabulously Create Server"
PRISM_DIR="$ROOT/dist/Fabulously Create"

read_pack_version() {
  grep '^version' "$PACK_DIR/pack.toml" | sed 's/.*"\(.*\)".*/\1/'
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

PACK_VERSION="$(read_pack_version)"

if [[ -n "${EXPECTED_VERSION:-}" && "$EXPECTED_VERSION" != "$PACK_VERSION" ]]; then
  echo "Version mismatch: EXPECTED_VERSION=$EXPECTED_VERSION, pack.toml=$PACK_VERSION" >&2
  exit 1
fi

require_command python3
require_command curl
require_command zip
require_command packwiz

MRPACK="$RELEASE_DIR/Fabulously-Create-${PACK_VERSION}.mrpack"
SERVER_ZIP="$RELEASE_DIR/Fabulously-Create-Server-${PACK_VERSION}.zip"
PRISM_ZIP="$RELEASE_DIR/Fabulously-Create-Prism-${PACK_VERSION}.zip"

echo "Building release v${PACK_VERSION}"
echo "  Output: $RELEASE_DIR"
echo ""

rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

echo "==> Refreshing pack index"
(
  cd "$PACK_DIR"
  packwiz refresh
)

echo ""
echo "==> Building server pack"
"$ROOT/scripts/build-server-pack.sh"

echo ""
echo "==> Building Prism client instance"
"$ROOT/scripts/build-prism-instance.sh"

echo ""
echo "==> Exporting Modrinth .mrpack"
(
  cd "$PACK_DIR"
  packwiz modrinth export -o "$MRPACK"
)

echo ""
echo "==> Zipping server pack"
(
  cd "$ROOT/dist"
  zip -rq "$SERVER_ZIP" "Fabulously Create Server"
)

echo ""
echo "==> Zipping Prism instance"
(
  cd "$ROOT/dist"
  zip -rq "$PRISM_ZIP" "Fabulously Create"
)

echo ""
echo "Release artifacts:"
ls -lh "$RELEASE_DIR"
echo ""
echo "Done. Upload dist/release/* to GitHub Releases and Modrinth."
