from playwright.sync_api import sync_playwright

def get_environment():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://kamigame.jp/onepiece-bountyrush/page/263853947595306109.html")
        page.wait_for_load_state("networkidle")

        # 💡 ヘッダーを非表示にする
        page.evaluate("""() => {
            const header = document.querySelector('.kamigame-layout-dropmenu-header');
            if (header) header.style.display = 'none';
        }""")

        page.evaluate("""() => {
            const ad = document.getElementById("overlay_ad_pc");
            if (ad) ad.style.display = 'none';
        }""")

        # 対象テキストを含む要素を探す
        element = page.query_selector(".tier-table")

        # その要素のスクリーンショットを保存
        element.screenshot(path="ranking_clean.png")

        browser.close()
