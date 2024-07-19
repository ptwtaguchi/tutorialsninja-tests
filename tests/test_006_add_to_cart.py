import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.helpers import log_execution_time

PRODUCT_NAME = "iPhone"

@pytest.mark.usefixtures("page")
class TestAddToCart:
    @log_execution_time
    def test_add_to_cart(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)

        home_page.open()
        home_page.search_product(PRODUCT_NAME)
        home_page.select_product(PRODUCT_NAME)
        
        product_page.add_to_cart()
        
        try:
            assert product_page.is_product_added_to_cart()
        except Exception as e:
            # 失敗時にスクリーンショットを保存
            page.screenshot(path="add_to_cart_failure.png")
            # 失敗時にページのHTMLを保存
            with open("add_to_cart_failure.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            raise e
