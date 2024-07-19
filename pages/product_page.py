from playwright.sync_api import Page
from utils.constants import TIMEOUT

class ProductPage:
    def __init__(self, page: Page):
        self.page = page

    def add_to_cart(self):
        self.page.wait_for_selector("button#button-cart", timeout=TIMEOUT)
        self.page.click("button#button-cart")
        self.page.wait_for_selector("div.alert-success", timeout=TIMEOUT)

    def is_product_added_to_cart(self):
        return self.page.is_visible("div.alert-success")
