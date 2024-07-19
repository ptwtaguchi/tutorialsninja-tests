import pytest
from utils.helpers import log_execution_time

@pytest.mark.usefixtures("page")
class TestNavigationAndPages:
    @log_execution_time
    def test_navigation_and_pages(self, page):
        # このテストは別のツールで実施します。
        pass
