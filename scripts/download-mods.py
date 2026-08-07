#!/usr/bin/env python3
"""Download mods and configs from a packwiz pack into a Minecraft directory."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import urllib.request
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


DEFAULT_WORKERS = 8
USER_AGENT = "fabulously-create/1.0"


@dataclass(frozen=True)
class DownloadTask:
    name: str
    url: str
    dest: Path
    expected_hash: str | None
    hash_fmt: str | None


@dataclass(frozen=True)
class DownloadResult:
    dest: Path
    status: str


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


def curseforge_download_url(file_id: int, filename: str) -> str:
    encoded_filename = quote(filename, safe="")
    return f"https://edge.forgecdn.net/files/{file_id // 1000}/{file_id % 1000}/{encoded_filename}"


def resolve_download(meta: dict) -> tuple[str | None, str | None, str | None]:
    download = meta.get("download", {})
    url = download.get("url")
    expected_hash = download.get("hash")
    hash_fmt = download.get("hash-format")

    if url:
        return url, expected_hash, hash_fmt

    if download.get("mode") == "metadata:curseforge":
        update = meta.get("update", {}).get("curseforge", {})
        file_id = update.get("file-id")
        filename = meta.get("filename")
        if file_id and filename:
            return curseforge_download_url(int(file_id), filename), expected_hash, hash_fmt

    return None, expected_hash, hash_fmt


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


def download_file(task: DownloadTask) -> DownloadResult:
    task.dest.parent.mkdir(parents=True, exist_ok=True)
    if task.dest.exists():
        return DownloadResult(task.dest, f"skip (exists): {task.dest.name}")

    req = urllib.request.Request(task.url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()

    if task.expected_hash and task.hash_fmt and not verify_hash(
        data, task.expected_hash, task.hash_fmt
    ):
        raise RuntimeError(f"hash mismatch for {task.dest.name}")

    task.dest.write_bytes(data)
    return DownloadResult(task.dest, f"download: {task.dest.name}")


def download_files(tasks: list[DownloadTask], workers: int) -> list[str]:
    if not tasks:
        return []

    messages: list[str] = []
    if workers <= 1 or len(tasks) == 1:
        for task in tasks:
            try:
                result = download_file(task)
            except Exception as exc:
                raise RuntimeError(f"{task.dest.name}: {exc}") from exc
            messages.append(result.status)
        return messages

    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(download_file, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                errors.append(f"{task.dest.name}: {exc}")
                continue
            messages.append(result.status)

    if errors:
        raise RuntimeError("download failed:\n  " + "\n  ".join(sorted(errors)))

    return sorted(messages, key=lambda line: line.split(": ", 1)[-1])


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


def copy_datapacks(pack_dir: Path, output: Path) -> None:
    datapacks_src = pack_dir / "datapacks"
    if not datapacks_src.is_dir():
        return

    dest = output / "datapacks"
    import shutil

    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(datapacks_src, dest, dirs_exist_ok=True)


def copy_server_configs(pack_dir: Path, output: Path) -> None:
    """Copy only configs useful on a dedicated server."""
    import shutil

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

    # Pack-authored quest book must be on the dedicated server.
    quests_src = config_src / "ftbquests"
    if quests_src.is_dir():
        quests_dest = dest / "ftbquests"
        if quests_dest.exists():
            shutil.rmtree(quests_dest, ignore_errors=True)
        shutil.copytree(quests_src, quests_dest)
        print("  config: ftbquests/")


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
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Parallel download workers (default: {DEFAULT_WORKERS})",
    )
    args = parser.parse_args()

    if args.workers < 1:
        print("error: --workers must be at least 1", file=sys.stderr)
        return 1

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
    tasks: list[DownloadTask] = []
    seen_dest: set[Path] = set()
    for pw_path, category in collect_pw_files(pack_dir):
        meta = parse_pw_toml(pw_path)
        name = meta.get("name", pw_path.stem)

        if not should_include(pw_path, category, args.profile, denylist, meta):
            skipped += 1
            continue

        filename = meta["filename"]
        url, expected_hash, hash_fmt = resolve_download(meta)
        dest = (mods_dir if category == "mods" else rp_dir) / filename
        if dest in seen_dest:
            continue
        seen_dest.add(dest)

        # Local/bundled mods: jar lives next to the .pw.toml (no download URL).
        if not url:
            local_jar = pw_path.parent / filename
            if not local_jar.is_file():
                print(f"skip (no url/local jar): {name}", file=sys.stderr)
                skipped += 1
                seen_dest.discard(dest)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and dest.samefile(local_jar):
                print(f"  skip (local): {dest.name}")
            else:
                data = local_jar.read_bytes()
                if expected_hash and hash_fmt and not verify_hash(
                    data, expected_hash, hash_fmt
                ):
                    print(f"  error: hash mismatch for local {dest.name}", file=sys.stderr)
                    return 1
                shutil.copy2(local_jar, dest)
                print(f"  copy (local): {dest.name}")
            continue

        tasks.append(
            DownloadTask(
                name=name,
                url=url,
                dest=dest,
                expected_hash=expected_hash,
                hash_fmt=hash_fmt,
            )
        )

    try:
        for line in download_files(tasks, args.workers):
            print(f"  {line}")
    except RuntimeError as exc:
        print(f"  error: {exc}", file=sys.stderr)
        return 1

    if args.profile == "server":
        print("\nCopying server configs...")
        copy_server_configs(pack_dir, output)
        print("Copying datapacks...")
        copy_datapacks(pack_dir, output)
    else:
        print("\nCopying configs...")
        copy_all_configs(pack_dir, output)
        print("Copying datapacks...")
        copy_datapacks(pack_dir, output)

    mod_count = len(list(mods_dir.glob("*.jar")))
    print(f"\nDone. {mod_count} mods in {mods_dir}")
    if args.profile == "server":
        print(f"Skipped {skipped} client-only entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
