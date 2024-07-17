from pages.base_page import BasePage

class ProductPage(BasePage):
    def add_to_cart(self):
        self.page.click("button#button-cart")

    def get_text(self, selector):
        return self.page.text_content(selector)
