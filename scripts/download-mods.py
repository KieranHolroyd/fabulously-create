#!/usr/bin/env python3
"""Download mods and configs from a packwiz pack into a Minecraft directory."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import urllib.request
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


def parse_pw_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def load_denylist(path: Path) -> set[str]:
    entries: set[str] = set()
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            entries.add(line)
    return entries


def verify_hash(data: bytes, expected: str, fmt: str) -> bool:
    if fmt == "sha512":
        actual = hashlib.sha512(data).hexdigest()
    elif fmt == "sha256":
        actual = hashlib.sha256(data).hexdigest()
    elif fmt == "sha1":
        actual = hashlib.sha1(data).hexdigest()
    else:
        print(f"  warning: unknown hash format {fmt}, skipping verification", file=sys.stderr)
        return True
    return actual == expected


def download_file(url: str, dest: Path, expected_hash: str | None, hash_fmt: str | None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  skip (exists): {dest.name}")
        return

    print(f"  download: {dest.name}")
    req = urllib.request.Request(url, headers={"User-Agent": "fabulously-create/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()

    if expected_hash and hash_fmt and not verify_hash(data, expected_hash, hash_fmt):
        raise RuntimeError(f"hash mismatch for {dest.name}")

    dest.write_bytes(data)


def collect_pw_files(pack_dir: Path) -> list[tuple[Path, str]]:
    entries: list[tuple[Path, str]] = []
    for subdir, category in [("mods", "mods"), ("resourcepacks", "resourcepacks")]:
        folder = pack_dir / subdir
        if folder.is_dir():
            for path in sorted(folder.glob("*.pw.toml")):
                entries.append((path, category))
    return entries


def mod_stem(pw_path: Path) -> str:
    name = pw_path.name
    if name.endswith(".pw.toml"):
        return name[: -len(".pw.toml")]
    return pw_path.stem


def should_include(
    pw_path: Path,
    category: str,
    profile: str,
    denylist: set[str],
    meta: dict,
) -> bool:
    stem = mod_stem(pw_path)
    side = meta.get("side", "both")

    if profile == "server":
        if category == "resourcepacks":
            return False
        if stem in denylist:
            return False
        if side == "client":
            return False
        return True

    if profile == "client":
        if side == "server":
            return False
        return True

    return True


def copy_server_configs(pack_dir: Path, output: Path) -> None:
    """Copy only configs useful on a dedicated server."""
    config_src = pack_dir / "config"
    if not config_src.is_dir():
        return

    dest = output / "config"
    dest.mkdir(parents=True, exist_ok=True)

    for name in ("fabric_loader_dependencies.json",):
        src = config_src / name
        if src.is_file():
            shutil.copy2(src, dest / name)
            print(f"  config: {name}")


def copy_all_configs(pack_dir: Path, output: Path) -> None:
    config_src = pack_dir / "config"
    if not config_src.is_dir():
        return
    dest = output / "config"
    import shutil

    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(config_src, dest, dirs_exist_ok=True)


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        default="instance/.minecraft",
        help="Target game directory (default: instance/.minecraft)",
    )
    parser.add_argument(
        "--pack-dir",
        default=str(scripts_dir.parent / "pack"),
        help="Path to packwiz pack directory",
    )
    parser.add_argument(
        "--profile",
        choices=("client", "server", "full"),
        default="full",
        help="full = all mods; server = dedicated server subset; client = all mods (alias for full)",
    )
    parser.add_argument(
        "--denylist",
        default=str(scripts_dir / "server-mod-denylist.txt"),
        help="Server denylist file (used with --profile server)",
    )
    args = parser.parse_args()

    pack_dir = Path(args.pack_dir).resolve()
    output = Path(args.output).resolve()
    mods_dir = output / "mods"
    rp_dir = output / "resourcepacks"
    denylist = load_denylist(Path(args.denylist)) if args.profile == "server" else set()

    if not (pack_dir / "pack.toml").is_file():
        print(f"error: no pack.toml in {pack_dir}", file=sys.stderr)
        return 1

    print(f"Pack: {pack_dir}")
    print(f"Output: {output}")
    print(f"Profile: {args.profile}\n")

    skipped = 0
    for pw_path, category in collect_pw_files(pack_dir):
        meta = parse_pw_toml(pw_path)
        name = meta.get("name", pw_path.stem)

        if not should_include(pw_path, category, args.profile, denylist, meta):
            skipped += 1
            continue

        filename = meta["filename"]
        download = meta.get("download", {})
        url = download.get("url")
        if not url:
            print(f"skip (no url): {name}")
            continue

        dest = (mods_dir if category == "mods" else rp_dir) / filename
        try:
            download_file(url, dest, download.get("hash"), download.get("hash-format"))
        except Exception as exc:
            print(f"  error: {exc}", file=sys.stderr)
            return 1

    if args.profile == "server":
        print("\nCopying server configs...")
        copy_server_configs(pack_dir, output)
    else:
        print("\nCopying configs...")
        copy_all_configs(pack_dir, output)

    mod_count = len(list(mods_dir.glob("*.jar")))
    print(f"\nDone. {mod_count} mods in {mods_dir}")
    if args.profile == "server":
        print(f"Skipped {skipped} client-only entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
