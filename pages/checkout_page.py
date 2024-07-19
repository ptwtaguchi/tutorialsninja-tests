from playwright.sync_api import Page
from utils.constants import TIMEOUT

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def proceed_to_checkout(self):
        self.page.click("a[href$='route=checkout/checkout']")
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_selector("div#content h1:has-text('Checkout')", timeout=TIMEOUT)

    def is_checkout_page_visible(self):
        return self.page.is_visible("div#content h1:has-text('Checkout')")

    def is_cart_page_visible(self):
        return self.page.is_visible("div#content h1:has-text('Shopping Cart')")

    def is_stock_unavailable(self):
        return self.page.is_visible("text=Products marked with *** are not available in the desired quantity or not in stock!")
