from playwright.sync_api import Page
from utils.helpers import generate_unique_email
from utils.constants import TIMEOUT

class AccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.registered_email = generate_unique_email()
        self.registered_password = "password"

    def register_user(self, first_name="Test", last_name="User", email=None, telephone="123456789", password=None):
        if email is None:
            email = self.registered_email
        if password is None:
            password = self.registered_password

        self.page.fill("input[name='firstname']", first_name)
        self.page.fill("input[name='lastname']", last_name)
        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='telephone']", telephone)
        self.page.fill("input[name='password']", password)
        self.page.fill("input[name='confirm']", password)
        self.page.check("input[name='agree']")
        self.page.click("input[type='submit'][value='Continue']")
        self.page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')", timeout=TIMEOUT)

    def login(self, email=None, password=None):
        if email is None:
            email = self.registered_email
        if password is None:
            password = self.registered_password

        self.page.fill("input[name='email']", email)
        self.page.fill("input[name='password']", password)
        self.page.click("input[type='submit'][value='Login']")
        self.page.wait_for_selector("div#content h2:has-text('My Account')", timeout=TIMEOUT)

    def logout(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_selector("a.list-group-item[href$='route=account/logout']:visible", timeout=TIMEOUT)
        self.page.click("a.list-group-item[href$='route=account/logout']")
        self.page.wait_for_selector("div#content h1:has-text('Account Logout')", timeout=TIMEOUT)

    def is_logged_out(self):
        return self.page.is_visible("div#content h1:has-text('Account Logout')")

    def is_logged_in(self):
        try:
            self.page.wait_for_selector("a.list-group-item[href$='route=account/logout']:visible", timeout=TIMEOUT)
            return True
        except TimeoutError:
            return False

    def reset_password(self, email):
        self.page.click("a[href$='route=account/forgotten']")
        self.page.fill("input[name='email']", email)
        self.page.click("input[type='submit'][value='Continue']")
        self.page.wait_for_selector("text=An email with a confirmation link has been sent your email address.", timeout=TIMEOUT)

    def is_account_created(self):
        return self.page.is_visible("div#content h1:has-text('Your Account Has Been Created!')")

    def is_password_reset(self):
        return self.page.is_visible("text=An email with a confirmation link has been sent your email address.")
