from playwright.sync_api import Page

class ProductPage:
    def __init__(self, page):
        self.page = page

    def add_to_cart(self):
        self.page.click("button#button-cart")
        self.page.wait_for_selector("div.alert-success", timeout=20000)  # タイムアウトを延長

    def is_product_added_to_cart(self):
        return self.page.is_visible("div.alert-success")
