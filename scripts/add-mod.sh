#!/usr/bin/env bash
# Add a mod to the packwiz manifest. Requires packwiz on PATH or in ~/go/bin.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$ROOT/pack"
PACKWIZ="${PACKWIZ:-$(command -v packwiz || echo "$HOME/go/bin/packwiz")}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <modrinth-slug> [version-id]"
  echo "Example: $0 create-fly"
  echo "Example: $0 journeymap 6Np0S5K2"
  exit 1
fi

slug="$1"
version_id="${2:-}"

if [[ ! -x "$PACKWIZ" && ! -f "$PACKWIZ" ]]; then
  echo "packwiz not found. Install with: go install github.com/packwiz/packwiz@latest"
  exit 1
fi

cd "$PACK_DIR"
project_id="$(curl -fsSL "https://api.modrinth.com/v2/project/$slug" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")"

if [[ -n "$version_id" ]]; then
  "$PACKWIZ" -y modrinth add --project-id "$project_id" --version-id "$version_id"
else
  "$PACKWIZ" -y modrinth add "$slug"
fi

"$PACKWIZ" refresh
echo "Added $slug. Run scripts/download-mods.py to fetch jars."
