from playwright.sync_api import sync_playwright


def test_transfer_submission():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open login page
        page.goto("http://127.0.0.1:8001/login")

        # Login using demo credentials
        page.locator("input[name='username']").fill(
            "demo@creditunion.test"
        )
        page.locator("input[name='password']").fill("demo123")
        page.get_by_role(
            "button",
            name="Sign In to Dashboard"
        ).click()

        # Confirm dashboard loaded
        page.wait_for_url("**/dashboard")

        # Fill transfer form
        page.locator("input[name='account_number']").fill(
            "123456789"
        )
        page.locator("input[name='amount']").fill("100")

        # Submit transfer
        page.get_by_role(
            "button",
            name="Review and Submit Transfer"
        ).click()

        # Verify success message
        success_message = page.locator("#success-message")
        success_message.wait_for()

        assert "submitted successfully" in success_message.inner_text()

        page.screenshot(
            path="evidence/discovery/transfer-success.png",
            full_page=True
        )

        browser.close()