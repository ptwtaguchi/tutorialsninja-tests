import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestUserLoginLogout:
    @log_execution_time
    def test_user_login_logout(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)
    
        home_page.go_to_register_page()
        account_page.register_user()
        account_page.logout()
        assert account_page.is_logged_out()
        home_page.go_to_login_page()
        account_page.login(email=account_page.registered_email, password=account_page.registered_password)
        assert account_page.is_logged_in()
