import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestUserRegistration:
    @log_execution_time
    def test_user_registration(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)
    
        home_page.go_to_register_page()
        account_page.register_user()
        assert account_page.is_account_created()
