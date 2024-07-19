import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestPasswordReset:
    @log_execution_time
    def test_password_reset(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)
    
        home_page.go_to_register_page()
        account_page.register_user()
        account_page.logout()
        home_page.go_to_login_page()
        account_page.reset_password(email=account_page.registered_email)
        assert account_page.is_password_reset()
