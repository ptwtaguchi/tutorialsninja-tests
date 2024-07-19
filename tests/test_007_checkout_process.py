import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.helpers import log_execution_time

PRODUCT_NAME = "iPhone"

@pytest.mark.usefixtures("page")
class TestCheckoutProcess:
    @log_execution_time
    def test_checkout_process(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        home_page.open()
        home_page.search_product(PRODUCT_NAME)
        home_page.select_product(PRODUCT_NAME)
        
        product_page.add_to_cart()
        
        home_page.go_to_cart()
        
        try:
            assert cart_page.is_stock_unavailable()
        except Exception as e:
            # 失敗時にスクリーンショットを保存
            page.screenshot(path="checkout_process_failure.png")
            # 失敗時にページのHTMLを保存
            with open("checkout_process_failure.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            raise e
