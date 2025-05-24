from playwright.async_api import async_playwright

async def get_environment():
    print("Fetching environment information...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://kamigame.jp/onepiece-bountyrush/page/263853947595306109.html", wait_until="networkidle")

        # すべての画像が読み込まれるまで待つ
        await page.evaluate("""
            () => Promise.all(Array.from(document.images).map(img => {
                if (img.complete) return Promise.resolve();
                return new Promise(resolve => {
                    img.addEventListener('load', resolve);
                    img.addEventListener('error', resolve);
                });
            }))
        """)


        element = await page.query_selector('.tier-table')  # 例: '#main' や '.header'など
        await element.screenshot(path='partial_screenshot.png')

        await browser.close()
