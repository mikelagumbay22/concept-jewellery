#!/usr/bin/env python3
"""One-pass build: src/ -> dist/ (static files as-is) + .nojekyll. Pages already use relative paths only."""
import shutil
from pathlib import Path
H = Path(__file__).resolve().parent
dist = H / "dist"
if dist.exists():
    shutil.rmtree(dist)
shutil.copytree(H / "src", dist)
(dist / ".nojekyll").write_bytes(b"")
print("built", sum(1 for _ in dist.rglob("*") if _.is_file()), "files,", round(sum(f.stat().st_size for f in dist.rglob("*") if f.is_file()) / 1048576, 2), "MB ->", dist)
