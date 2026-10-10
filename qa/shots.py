"""3 JPG shots (<1 MB) at scroll points of a pinned section + CLS + reduced-motion probe.
Usage: shots.py URL SELECTOR OUTDIR p1 p2 p3 [mobile_index]"""
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
CHROME = "/usr/bin/google-chrome"
URL, SEL, OUT = sys.argv[1:4]; PS = [float(x) for x in sys.argv[4:7]]; MOB = int(sys.argv[7]) if len(sys.argv) > 7 else -1
CLS = "window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})"
def go(pg, p):
    target = pg.evaluate("([s,p])=>{const el=document.querySelector(s);return el.offsetTop+p*Math.max(0,el.offsetHeight-innerHeight)}", [SEL, p])
    cur = pg.evaluate("scrollY")
    for k in range(1, 9): pg.evaluate("y=>scrollTo(0,y)", cur + (target - cur) * k / 8); pg.wait_for_timeout(120)
    pg.wait_for_timeout(900)
def save(pg, name):
    pg.screenshot(path="/tmp/_c.png"); im = Image.open("/tmp/_c.png").convert("RGB"); q = 84
    while True:
        im.save(f"{OUT}/{name}", quality=q, optimize=True)
        if os.path.getsize(f"{OUT}/{name}") < 1_000_000 or q < 50: break
        q -= 8
    print(f"{OUT}/{name}", os.path.getsize(f"{OUT}/{name}") // 1024, "KB")
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    d = b.new_page(viewport={"width": 1440, "height": 900}); d.add_init_script(CLS); d.goto(URL, wait_until="networkidle"); d.wait_for_timeout(1500)
    for i, q in enumerate(PS):
        if i == MOB: continue
        go(d, q); save(d, f"shot-{i + 1}.jpg")
    print("desktop CLS", round(d.evaluate("window.__cls"), 4))
    if MOB >= 0:
        m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True); m.add_init_script(CLS)
        m.goto(URL, wait_until="networkidle"); m.wait_for_timeout(1500); go(m, PS[MOB]); save(m, f"shot-{MOB + 1}.jpg"); print("mobile CLS", round(m.evaluate("window.__cls"), 4))
    r = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); r.goto(URL, wait_until="networkidle"); r.wait_for_timeout(800)
    print("reduced: running animations", r.evaluate("document.getAnimations().filter(a=>a.playState==='running').length"), "html class", r.evaluate("document.documentElement.className"), "section h", r.evaluate(f"document.querySelector('{SEL}').offsetHeight"))
    b.close()
