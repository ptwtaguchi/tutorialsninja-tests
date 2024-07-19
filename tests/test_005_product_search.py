import pytest
from pages.home_page import HomePage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestProductSearch:
    @log_execution_time
    def test_product_search(self, page):
        home_page = HomePage(page)
        home_page.search_product()
        assert home_page.is_product_search_successful()
