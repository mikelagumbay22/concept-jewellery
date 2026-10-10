"""Ban/rule checks for a Northpage design-concept page (dist/). Usage: python3 qa/bancheck.py <dist> <brand> <frame_budget_mb>"""
import re, sys, html as H
from pathlib import Path
D = Path(sys.argv[1]); BRAND = sys.argv[2]; FRAME_MB = float(sys.argv[3]) if len(sys.argv) > 3 else 0
BADGE_I, BADGE_V = "Illustrative AI image, concept only", "Illustrative AI video, concept only"
fails, out = [], []
def ok(c, m): out.append(("PASS " if c else "FAIL ") + m); c or fails.append(m)
pages = sorted(D.glob("*.html")); text = {f: f.read_text() for f in D.rglob("*") if f.suffix in (".html", ".css", ".js", ".svg")}
allt = "\n".join(text.values()); low = allt.lower()
ok((D / ".nojekyll").exists(), ".nojekyll")
ok(not re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", allt) and "mailto" not in low, "no e-mail / mailto")
ok("fonts.googleapis" not in low and "fonts.gstatic" not in low and "@font-face" in low, "self-hosted fonts only")
for name in ["octaboot", "sargi", "wearebrand", "samjho", "chicken", "bb jewel", "oks cars", "sadaf", "paint force", "tailoring for the few", "anatomy of a suit", "john"]:
    ok(name not in low, f"no '{name}' (refs / real clients)")
for f in pages:
    s = f.read_text(); n = f.name
    vis = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|head)\b.*?</\1>", " ", s, flags=re.S)))
    ok('<meta name="robots" content="noindex, nofollow">' in s, f"{n}: noindex")
    ok("Design concept by Northpage" in vis and "fictional brand" in vis, f"{n}: concept banner")
    ok("github.io" not in vis, f"{n}: no github.io in visible copy")
    ok(not re.search(r"\$\s?\d|€\s?\d|£\s?\d", vis), f"{n}: no prices")
    refs = re.findall(r'(?:href|src|poster|data-src)="([^"]+)"', s) + [u.split()[0] for ss in re.findall(r'srcset="([^"]+)"', s) for u in ss.split(",")]
    bad = [r for r in refs if r.startswith("/") or (not re.match(r"^(https?:|#|tel:)", r) and r != "./" and not (D / r.split("#")[0]).exists())]
    ok(not bad, f"{n}: refs relative + resolvable {bad[:3]}")
    for tag in re.findall(r"<(?:img|video|canvas)\b[^>]*>", s):
        ok(re.search(r'\swidth="\d+"', tag) and re.search(r'\sheight="\d+"', tag), f"{n}: media has width/height ({tag[:40]})")
    if n == "index.html":
        imgs = [t for t in re.findall(r"<img\b[^>]*>", s) if "icon" not in t]
        ok(s.count(BADGE_I) + s.count(BADGE_V) >= 1 and all(H.unescape(s).count(BADGE_I) >= len([i for i in imgs if 'class="film__poster"' not in i]) for _ in [0]), f"index: every image/video badged ({len(imgs)} imgs)")
        ok(BRAND in vis, f"index: brand '{BRAND}' shown")
if FRAME_MB:
    fr = list((D / "img/frames").glob("*.webp")); mb = sum(f.stat().st_size for f in fr) / 1048576
    ok(60 <= len(fr) <= 90 and mb < FRAME_MB, f"{len(fr)} frames, {mb:.2f} MB (< {FRAME_MB} MB)")
big = [(f.name, f.stat().st_size // 1024) for f in D.rglob("*") if f.suffix in (".webp", ".jpg", ".png") and "frames" not in f.parts and f.stat().st_size > 250_000]
ok(not big, f"stills/layers under 250 KB {big}")
print("\n".join(out)); print(f"\n{len(out) - len(fails)} passed, {len(fails)} failed")
