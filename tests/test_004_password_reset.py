import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time, generate_unique_email
from utils.constants import TIMEOUT

@pytest.mark.usefixtures("page")
class TestPasswordReset:
    @log_execution_time
    def test_password_reset(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)

        home_page.open()
        unique_email = generate_unique_email()
        page.click("a[href$='account/account']")
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=TIMEOUT)

        home_page.go_to_register_page()
        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=TIMEOUT)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")

        page.goto("https://tutorialsninja.com/demo/index.php?route=account/login")
        page.wait_for_selector("a[href$='route=account/forgotten']", timeout=TIMEOUT)

        page.click("a[href$='route=account/forgotten']")
        page.wait_for_selector("input[name='email']", timeout=TIMEOUT)

        page.fill("input[name='email']", unique_email)
        page.click("input[type='submit']")

        page.wait_for_selector("div.alert.alert-success.alert-dismissible:has-text('An email with a confirmation link has been sent your email address.')", timeout=TIMEOUT)
        assert "An email with a confirmation link has been sent your email address." in account_page.get_text("div.alert.alert-success.alert-dismissible")
