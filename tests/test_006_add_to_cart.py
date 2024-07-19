import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestAddToCart:
    @log_execution_time
    def test_add_to_cart(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)
    
        home_page.search_product()
        home_page.select_product()
        product_page.add_to_cart()
        assert product_page.is_product_added_to_cart()
