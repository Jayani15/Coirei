from agent.tools import *
from utils.screenshot import take_screenshot

class WebTestingAgent:

    def __init__(self):
        self.page = None
        self.browser = None
        self.playwright = None

    def run(self, url):
        # Step 1: Open Website
        self.page, self.browser, self.playwright = open_website(url)

        # Step 2: Extract links
        links = get_all_links(self.page)

        # Step 3: Check broken links
        broken_links = check_broken_links(links)

        # Step 4: Test buttons
        button_results = click_buttons(self.page)

        # Step 5: Fill forms
        fill_forms(self.page)

        # Step 6: Screenshot
        screenshot = take_screenshot(self.page)

        # Cleanup
        self.browser.close()
        self.playwright.stop()

        return {
            "broken_links": broken_links,
            "button_results": button_results,
            "screenshot": screenshot
        }