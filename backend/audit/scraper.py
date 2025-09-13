from playwright.sync_api import sync_playwright
import base64
def scrape_page(url, timeout=45000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1280,'height':900})
        page.goto(url, timeout=timeout, wait_until='networkidle')
        page.wait_for_timeout(1000)
        html = page.content()
        title = page.title()
        meta = page.evaluate("""() => {
            const m = {};
            document.querySelectorAll('meta').forEach(x => {
                const k = x.getAttribute('name') || x.getAttribute('property') || '';
                if (k) m[k] = x.getAttribute('content');
            });
            return m;
        }""")
        screenshot = page.screenshot(full_page=True)
        screenshot_b64 = base64.b64encode(screenshot).decode()
        visible_text = page.evaluate("""() => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let node, text = '';
            while (node = walker.nextNode()) {
                if (node.textContent) text += node.textContent + '\\n';
            }
            return text;
        }""")
        browser.close()
        return {'html': html, 'title': title, 'meta': meta, 'screenshot_b64': screenshot_b64, 'visible_text': visible_text}
