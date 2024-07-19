import pytest
from pages.home_page import HomePage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestProductSearch:
    @log_execution_time
    def test_product_search(self, page):
        # 1. ホームページを開く
        home_page = HomePage(page)

        # 2. 商品検索を実行する
        home_page.search_product()

        # 3. 商品検索が成功したことを確認する
        assert_with_screenshot(page, home_page.is_product_search_successful())
