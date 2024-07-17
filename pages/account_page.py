from .base_page import BasePage

class AccountPage(BasePage):
    def register_user(self, firstname, lastname, email, telephone, password):
        self.page.fill("input[name='firstname']", firstname)
        self.page.fill("input[name='lastname']", lastname)
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='telephone']", telephone)
        self.page.fill("input[name='password']", password)
        self.page.fill("input[name='confirm']", password)
        self.page.check("input[name='agree']")
        self.page.click("input[type='submit'][value='Continue']")

    def login(self, email, password):
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='password']", password)
        self.page.click("input[type='submit'][value='Login']")

    def reset_password(self, email):
        self.page.click("a[href$='route=account/forgotten']")
        self.page.fill("input[name='email']", email)
        self.page.click("input[type='submit'][value='Continue']")

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector)
