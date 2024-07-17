from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def fill_billing_details(self, first_name, last_name, address, city, postcode, country, region, email, telephone):
        self.page.fill("input[name='firstname']", first_name)
        self.page.fill("input[name='lastname']", last_name)
        self.page.fill("input[name='address_1']", address)
        self.page.fill("input[name='city']", city)
        self.page.fill("input[name='postcode']", postcode)
        self.page.select_option("select[name='country_id']", label=country)
        self.page.select_option("select[name='zone_id']", label=region)
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='telephone']", telephone)
        self.page.click("input#button-payment-address")
    
    def select_shipping_method(self, method):
        self.page.click(f"input[value='{method}']")
        self.page.click("input#button-shipping-method")
    
    def select_payment_method(self, method):
        self.page.click(f"input[value='{method}']")
        self.page.check("input[name='agree']")
        self.page.click("input#button-payment-method")
    
    def confirm_order(self):
        self.page.click("input#button-confirm")
