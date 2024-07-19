import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestUserRegistration:
    @log_execution_time
    def test_user_registration(self, page):
        # 1. ホームページを開き、登録ページに移動する
        home_page = HomePage(page)
        home_page.go_to_register_page()

        # 2. アカウントページでユーザーを登録する
        account_page = AccountPage(page)
        account_page.register_user()

        # 3. アカウントが作成されたことを確認する
        assert_with_screenshot(page, account_page.is_account_created())
