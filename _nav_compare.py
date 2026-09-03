import asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ORIG = "https://www.carbonitav.com/%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D0%B0-%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0home-page"
CLONE = "https://relamnpc.github.io/carbonitav-clone/index.html"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for label, url in [("ORIG", ORIG), ("CLONE", CLONE)]:
            page = await browser.new_page(viewport={"width":1920,"height":1080})
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
            try:
                r = page.locator("button:has-text('Reject')")
                if await r.count()>0: await r.click(); await asyncio.sleep(1)
            except: pass

            nav = await page.evaluate("""() => {
                // Top navigation container
                const topNav = document.querySelector('.TBNRv, .X68jTe, .MceBjb, header, nav, [role="banner"]');
                let navRect = null;
                if (topNav) {
                    const r = topNav.getBoundingClientRect();
                    navRect = {h: r.height, y: r.y, top: r.top};
                }
                // The sticky header that scrolls
                const header = document.querySelector('.STa31e, .m3F2Gd, .VjX08f, .tmemWc, .yaqOZd');
                
                // Find all elements near top
                const tops = [];
                document.querySelectorAll('body > *, section, .yaqOZd').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.top > -5 && r.top < 200) {
                        tops.push({tag: el.tagName, cls: (el.className||'').toString().substring(0,25), top: Math.round(r.top), h: Math.round(r.height)});
                    }
                });
                tops.sort((a,b)=>a.top-b.top);
                return {navRect, tops: tops.slice(0,10)};
            }""")
            print(f"\n=== {label} ===")
            print(nav)
            await page.close()

        await browser.close()

asyncio.run(main())
