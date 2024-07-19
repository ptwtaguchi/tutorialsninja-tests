import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestCheckoutProcess:
    @log_execution_time
    def test_checkout_process(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)
        checkout_page = CheckoutPage(page)

        home_page.search_product()
        home_page.select_product()
        product_page.add_to_cart()
        home_page.go_to_cart()
        assert checkout_page.is_stock_unavailable()
