import pytest
from pages.home_page import HomePage
from pages.account_page import AccountPage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestUserLoginLogout:
    @log_execution_time
    def test_user_login_logout(self, page):
        # 1. ホームページを開く
        home_page = HomePage(page)
        account_page = AccountPage(page)

        # 2. ユーザー登録ページに遷移する
        home_page.go_to_register_page()

        # 3. ユーザーを登録する
        account_page.register_user()

        # 4. ログアウトする
        account_page.logout()

        # 5. ログアウトが成功したことを確認する
        assert_with_screenshot(page, account_page.is_logged_out())

        # 6. ログインページに遷移する
        home_page.go_to_login_page()

        # 7. ログインする
        account_page.login(email=account_page.registered_email, password=account_page.registered_password)

        # 8. ログインが成功したことを確認する
        assert_with_screenshot(page, account_page.is_logged_in())
