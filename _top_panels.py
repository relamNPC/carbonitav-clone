import asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ORIG = "https://www.carbonitav.com/%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D0%B0-%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0home-page"
CLONE = "https://relamnpc.github.io/carbonitav-clone/index.html"

async def check(browser, label, url):
    page = await browser.new_page(viewport={"width":1920,"height":1080})
    await page.goto(url, wait_until="networkidle", timeout=60000)
    await asyncio.sleep(3)
    try:
        r = page.locator("button:has-text('Reject')")
        if await r.count()>0: await r.click(); await asyncio.sleep(1)
    except: pass
    data = await page.evaluate("""() => {
        const selectors = ['.vB4mjb','.p9b27','.M63kCb','.BuY5Fd','.TbNlJb','.DXsoRd','.JzO0Vc'];
        const res = {};
        selectors.forEach(s=>{
            const el = document.querySelector(s);
            if (el) {
                const r = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                res[s] = {top: Math.round(r.top), h: Math.round(r.height), pos: cs.position, disp: cs.display};
            } else res[s]=null;
        });
        // body margin/padding
        const bs = getComputedStyle(document.body);
        res['BODY'] = {mt: bs.marginTop, pt: bs.paddingTop, height: Math.round(document.body.getBoundingClientRect().height)};
        return res;
    }""")
    print(f"\n=== {label} ===")
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))
    await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        await check(browser, "ORIG", ORIG)
        await check(browser, "CLONE", CLONE)
        await browser.close()

asyncio.run(main())
