from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page

    def is_cart_page_visible(self):
        return self.page.is_visible("div#content h1:has-text('Shopping Cart')")

    def is_stock_unavailable(self):
        return self.page.is_visible("text=Products marked with *** are not available in the desired quantity or not in stock!")
