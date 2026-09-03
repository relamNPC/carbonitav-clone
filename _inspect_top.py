import asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CLONE = "https://relamnpc.github.io/carbonitav-clone/index.html"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width":1920,"height":1080})
        await page.goto(CLONE, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(3)

        data = await page.evaluate("""() => {
            // walk top structure
            const out = [];
            document.querySelectorAll('body > div, body > *').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.top < 200) {
                    out.push({tag: el.tagName, cls: (el.className||'').toString().substring(0,40), top: Math.round(r.top), h: Math.round(r.height), st: (el.getAttribute('style')||'').substring(0,60)});
                }
            });
            // Also check position:fixed / sticky elements
            const fixed = [];
            document.querySelectorAll('*').forEach(el=>{
                const cs = getComputedStyle(el);
                if ((cs.position==='fixed'||cs.position==='sticky') && el.getBoundingClientRect().top < 100) {
                    const r = el.getBoundingClientRect();
                    fixed.push({tag: el.tagName, cls:(el.className||'').toString().substring(0,30), top:Math.round(r.top), h:Math.round(r.height), pos: cs.position});
                }
            });
            return {topEls: out.slice(0,6), fixed: fixed.slice(0,8)};
        }""")
        print("TOP ELEMENTS:")
        for e in data['topEls']:
            print("  ", e)
        print("\nFIXED/STICKY:")
        for e in data['fixed']:
            print("  ", e)
        await browser.close()

asyncio.run(main())
