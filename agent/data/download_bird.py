"""Download and unpack the BIRD dev set (databases + questions + gold SQL).

Usage (from repo root):
    uv run --project agent python agent/data/download_bird.py

The dev set zip is ~1-2 GB. The script streams the download with resume
support, unpacks it, and also unpacks the nested dev_databases.zip that
BIRD ships inside the outer archive.

Source: https://bird-bench.github.io/  (dev set hosted on Aliyun OSS)
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

BIRD_DEV_URL = "https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip"
DATA_DIR = Path(__file__).resolve().parent
ZIP_PATH = DATA_DIR / "dev.zip"
CHUNK = 1 << 20  # 1 MiB


def download(url: str, dest: Path) -> None:
    """Stream `url` to `dest`, resuming a partial download if one exists."""
    existing = dest.stat().st_size if dest.exists() else 0

    head = Request(url, method="HEAD")
    with urlopen(head) as resp:
        total = int(resp.headers.get("Content-Length", 0))

    if existing and existing == total:
        print(f"[skip] {dest.name} already fully downloaded ({total:,} bytes)")
        return

    req = Request(url)
    mode = "wb"
    if existing and existing < total:
        req.add_header("Range", f"bytes={existing}-")
        mode = "ab"
        print(f"[resume] continuing {dest.name} from byte {existing:,}")

    done = existing
    with urlopen(req) as resp, open(dest, mode) as f:
        while chunk := resp.read(CHUNK):
            f.write(chunk)
            done += len(chunk)
            pct = f"{done / total:6.1%}" if total else "?"
            print(f"\r[download] {done:,} / {total:,} bytes ({pct})", end="", flush=True)
    print()


def unpack(zip_path: Path, dest: Path) -> None:
    print(f"[unzip] {zip_path.name} -> {dest}")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)


def unpack_nested_zips(root: Path) -> None:
    """BIRD's dev.zip contains dev_databases.zip inside — unpack any nested zips."""
    for nested in root.rglob("*.zip"):
        if nested == ZIP_PATH:
            continue
        target = nested.parent / nested.stem
        if target.exists():
            print(f"[skip] {nested.name} already unpacked")
            continue
        unpack(nested, nested.parent)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        download(BIRD_DEV_URL, ZIP_PATH)
    except Exception as e:  # noqa: BLE001 - report and exit, rerun resumes
        print(f"\n[error] download failed: {e}", file=sys.stderr)
        print("Re-run this script to resume.", file=sys.stderr)
        sys.exit(1)

    unpack(ZIP_PATH, DATA_DIR)
    unpack_nested_zips(DATA_DIR)

    sqlite_files = list(DATA_DIR.rglob("*.sqlite"))
    json_files = [p.name for p in DATA_DIR.rglob("dev*.json")]
    print(f"\n[done] {len(sqlite_files)} SQLite databases, question files: {json_files}")


if __name__ == "__main__":
    main()
