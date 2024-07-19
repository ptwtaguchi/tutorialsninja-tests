import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time, generate_unique_email
from utils.constants import TIMEOUT

@pytest.mark.usefixtures("page")
class TestUserRegistration:
    @log_execution_time
    def test_user_registration(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)
        
        home_page.open()
        page.wait_for_load_state('load')
        page.wait_for_load_state('networkidle')
        page.click("a[href$='account/account']")
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=TIMEOUT)

        home_page.go_to_register_page()

        unique_email = generate_unique_email()
        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')", timeout=TIMEOUT)
        assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")
