import pytest
from pages.home_page import HomePage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestHomePage:
    @log_execution_time
    def test_home_page_display(self, page):
        # 1. ホームページを開く
        home_page = HomePage(page)
        
        # 2. ホームページが表示されていることを確認する
        assert_with_screenshot(page, home_page.is_home_page_visible())
