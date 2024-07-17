from .base_page import BasePage

class CartPage(BasePage):
    def go_to_checkout(self):
        self.click("a[href$='route=checkout/checkout']")
