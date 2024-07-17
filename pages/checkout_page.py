from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def proceed_to_checkout(self):
        self.page.click("a[href$='route=checkout/checkout']")
