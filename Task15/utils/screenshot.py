import os

def take_screenshot(page, name="screenshot.png"):
    os.makedirs("screenshots", exist_ok=True)
    path = f"screenshots/{name}"
    page.screenshot(path=path)
    return path