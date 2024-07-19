import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utils.helpers import log_execution_time, assert_with_screenshot

@pytest.mark.usefixtures("page")
class TestCheckoutProcess:
    @log_execution_time
    def test_checkout_process(self, page):
        # 1. ホームページを開く
        home_page = HomePage(page)

        # 2. 商品検索を実行する
        home_page.search_product()

        # 3. 検索結果から商品を選択する
        home_page.select_product()

        # 4. 商品をカートに追加する
        product_page = ProductPage(page)
        product_page.add_to_cart()

        # 5. カートに移動する
        home_page.go_to_cart()

        # 6. 在庫が不足しているか確認する
        checkout_page = CheckoutPage(page)
        assert_with_screenshot(page, checkout_page.is_stock_unavailable())
