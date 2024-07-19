import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time, generate_unique_email
from utils.constants import TIMEOUT

@pytest.mark.usefixtures("page")
class TestUserLoginLogout:
    @log_execution_time
    def test_user_login_logout(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)

        home_page.open()
        unique_email = generate_unique_email()
        page.click("a[href$='account/account']")
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=TIMEOUT)

        home_page.go_to_register_page()
        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')", timeout=TIMEOUT)
        assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")

        page.click("div.buttons a.btn.btn-primary")
        page.wait_for_selector("div#content h2:has-text('My Account')")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=TIMEOUT)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")

        try:
            sidebar_login = page.locator("aside#column-right a[href$='route=account/login']:visible").first
            sidebar_login.wait_for(timeout=TIMEOUT)
            sidebar_login.click()
        except Exception as e:
            print(f"Sidebar login error: {e}")
            raise

        page.wait_for_selector("h2:has-text('Returning Customer')")
        account_page.login(unique_email, "password")
        page.wait_for_selector("div#content h2:has-text('My Account')")
        assert "My Account" in account_page.get_text("div#content h2")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=TIMEOUT)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")
