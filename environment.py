from playwright.async_api import async_playwright

async def get_environment():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://kamigame.jp/onepiece-bountyrush/page/263853947595306109.html")
        await page.wait_for_load_state("networkidle")

        # 💡 ヘッダーを非表示にする
        await page.evaluate("""() => {
            const header = document.querySelector('.kamigame-layout-dropmenu-header');
            if (header) header.style.display = 'none';
        }""")

        await page.evaluate("""() => {
            const ad = document.getElementById("overlay_ad_pc");
            if (ad) ad.style.display = 'none';
        }""")

        # 対象テキストを含む要素を探す
        element = await page.query_selector(".tier-table")

        # その要素のスクリーンショットを保存
        await element.screenshot(path="ranking_clean.png")

        await browser.close()

        return "ranking_clean.png"