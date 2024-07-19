import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestAddToCart:
    @log_execution_time
    def test_add_to_cart(self, page):
        # 1. ホームページを開く
        home_page = HomePage(page)

        # 2. 商品検索を実行する
        home_page.search_product()

        # 3. 検索結果から商品を選択する
        home_page.select_product()

        # 4. 商品をカートに追加する
        product_page = ProductPage(page)
        product_page.add_to_cart()

        # 5. 商品がカートに追加されたことを確認する
        assert_with_screenshot(page, product_page.is_product_added_to_cart())
