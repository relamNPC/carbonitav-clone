import asyncio, sys
from playwright.async_api import async_playwright
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ORIG = "https://www.carbonitav.com"
CLONE = "https://relamnpc.github.io/carbonitav-clone"

PAGES = {
    "index": "/%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D0%B0-%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0home-page",
    "briquettes": "/%D0%B1%D1%80%D0%B8%D0%BA%D0%B5%D1%82briquettes",
    "about": "/%D0%BF%D1%80%D0%BE-%D0%BD%D0%B0%D1%81about-us",
    "contacts": "/%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B8contacts",
    "production": "/%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%86%D1%96%D1%8Fproduction",
}

FILES = {
    "index": "index.html",
    "briquettes": "briquettes.html",
    "about": "about.html",
    "contacts": "contacts.html",
    "production": "production.html",
}

async def compare_page(browser, name, slug):
    print(f"\n========== {name} ==========")

    orig_page = await browser.new_page(viewport={"width":1920,"height":1080})
    clone_page = await browser.new_page(viewport={"width":1920,"height":1080})

    # Origin
    await orig_page.goto(ORIG+slug, wait_until="networkidle", timeout=60000)
    await asyncio.sleep(3)
    try:
        r = orig_page.locator("button:has-text('Reject')")
        if await r.count()>0: await r.click(); await asyncio.sleep(1)
    except: pass

    # Clone
    await clone_page.goto(CLONE+"/"+FILES[name], wait_until="networkidle", timeout=60000)
    await asyncio.sleep(3)

    # Screenshots
    await orig_page.screenshot(path=rf"C:\Users\max\Desktop\сайт\_cmp_orig_{name}.png", full_page=True)
    await clone_page.screenshot(path=rf"C:\Users\max\Desktop\сайт\_cmp_clone_{name}.png", full_page=True)

    # Extract structural data
    def extract(pg):
        return pg.evaluate("""() => {
            const out = {sections: []};
            // Collect visible layout blocks with their bounding boxes
            document.querySelectorAll('.IFuOkc, .mYVXT, .oKdM2c, .nUp0td, section[id^="h."], .tyJCtd, .jXK9ad').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 50 && rect.height > 20) {
                    out.sections.push({
                        cls: (el.className||'').toString().substring(0,30),
                        x: Math.round(rect.x), y: Math.round(rect.y + window.scrollY),
                        w: Math.round(rect.width), h: Math.round(rect.height),
                        text: (el.innerText||'').trim().substring(0,40)
                    });
                }
            });
            // Fonts used
            out.bodyFont = getComputedStyle(document.body).fontFamily;
            out.fontSize = getComputedStyle(document.body).fontSize;
            out.bgColor = getComputedStyle(document.body).backgroundColor;
            return out;
        }""")

    orig_data = await extract(orig_page)
    clone_data = await extract(clone_page)

    print(f"  ORIG body font: {orig_data['bodyFont']}")
    print(f"  CLONE body font: {clone_data['bodyFont']}")
    print(f"  ORIG body size: {orig_data['fontSize']} / CLONE: {clone_data['fontSize']}")
    print(f"  ORIG sections: {len(orig_data['sections'])}, CLONE: {len(clone_data['sections'])}")

    print("\n  --- ORIG sections ---")
    for s in orig_data['sections'][:12]:
        print(f"    [{s['x']},{s['y']} {s['w']}x{s['h']}] {s['cls']}: {s['text'][:30]}")
    print("\n  --- CLONE sections ---")
    for s in clone_data['sections'][:12]:
        print(f"    [{s['x']},{s['y']} {s['w']}x{s['h']}] {s['cls']}: {s['text'][:30]}")

    await orig_page.close()
    await clone_page.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for name, slug in PAGES.items():
            try:
                await compare_page(browser, name, slug)
            except Exception as e:
                print(f"ERROR {name}: {e}")
        await browser.close()

asyncio.run(main())
