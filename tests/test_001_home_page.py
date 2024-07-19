import pytest
from pages.home_page import HomePage
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestHomePage:
    @log_execution_time
    def test_home_page_display(self, page):
        home_page = HomePage(page)
        assert home_page.is_home_page_visible()
