from playwright.sync_api import sync_playwright
import requests

def open_website(url):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)
    return page, browser, p


def get_all_links(page):
    return page.eval_on_selector_all(
        "a", "elements => elements.map(e => e.href)"
    )


def check_broken_links(links):
    broken = []
    for link in links:
        if not link:
            continue
        try:
            res = requests.get(link, timeout=5)
            if res.status_code >= 400:
                broken.append(link)
        except:
            broken.append(link)
    return broken


def click_buttons(page):
    buttons = page.query_selector_all("button")
    results = []

    for i, btn in enumerate(buttons):
        try:
            btn.click(timeout=3000)
            results.append(f"Button {i}: Success")
        except Exception as e:
            results.append(f"Button {i}: Failed - {str(e)}")

    return results


def fill_forms(page):
    inputs = page.query_selector_all("input")

    for inp in inputs:
        try:
            inp.fill("test")
        except:
            pass

    return "Forms filled"