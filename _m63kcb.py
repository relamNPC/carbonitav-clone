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
        styles = await page.evaluate("""() => {
            const el = document.querySelector('.M63kCb');
            if (!el) return 'not found';
            const cs = getComputedStyle(el);
            const own = {};
            for (const rule of [...document.styleSheets]) {
                try {
                    for (const r of rule.cssRules) {
                        if (r.selectorText && r.selectorText.includes('.M63kCb') && r.style) {
                            own[r.selectorText] = r.style.cssText;
                        }
                    }
                } catch(e){}
            }
            // position of parent
            const parent = el.parentElement;
            let par = null;
            if (parent) { const r=parent.getBoundingClientRect(); const pcs=getComputedStyle(parent); par={cls:(parent.className||'').toString().substring(0,30), top:Math.round(r.top), h:Math.round(r.height), transform:pcs.transform, pos:pcs.position}; }
            return {
                transform: cs.transform, top: cs.top, position: cs.position,
                margin: cs.margin, marginTop: cs.marginTop,
                computedStyleTop: getComputedStyle(el).top,
                ownRules: own,
                parent: par
            };
        }""")
        import json
        print(json.dumps(styles, indent=2, ensure_ascii=False))
        await browser.close()

asyncio.run(main())
