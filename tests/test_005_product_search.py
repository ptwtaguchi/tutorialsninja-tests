import pytest
from pages.home_page import HomePage
from utils.helpers import log_execution_time

PRODUCT_NAME = "iPhone"

@pytest.mark.usefixtures("page")
class TestProductSearch:
    @log_execution_time
    def test_product_search(self, page):
        home_page = HomePage(page)
        home_page.open()
        home_page.search_product(PRODUCT_NAME)
        assert home_page.is_product_search_successful(PRODUCT_NAME)
