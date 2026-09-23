from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://127.0.0.1:8001")

    print("Browser is open.")
    print("A human can now inspect or interact with the page.")
    input("Press Enter after human intervention to resume...")

    print("Automation resumed.")
    print("Current URL:", page.url)

    browser.close()