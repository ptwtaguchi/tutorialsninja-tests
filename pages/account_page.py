from playwright.sync_api import Page

class AccountPage:
    def __init__(self, page: Page):
        self.page = page

    def register_user(self, first_name, last_name, email, phone, password):
        self.page.fill("input[name='firstname']", first_name)
        self.page.fill("input[name='lastname']", last_name)
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='telephone']", phone)
        self.page.fill("input[name='password']", password)
        self.page.fill("input[name='confirm']", password)
        self.page.check("input[name='agree']")
        self.page.click("input[value='Continue']")
    
    def get_text(self, selector):
        return self.page.text_content(selector)

    def is_account_created(self):
        return self.page.is_visible("div#content h1:has-text('Your Account Has Been Created!')")

    def continue_to_account_page(self):
        self.page.click("div.buttons a.btn.btn-primary")

    def login(self, email, password):
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='password']", password)
        self.page.click("input[type='submit']")

    def is_logged_in(self):
        return self.page.is_visible("div#content h2:has-text('My Account')")

    def logout(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.click("a[href$='route=account/logout']:visible")

    def is_logged_out(self):
        return self.page.is_visible("div#content h1:has-text('Account Logout')")

    def reset_password(self, email):
        self.page.fill("input[name='email']", email)
        self.page.click("input[type='submit']")

    def is_password_reset(self):
        return self.page.is_visible("text=An email with a confirmation link has been sent your email address.")
