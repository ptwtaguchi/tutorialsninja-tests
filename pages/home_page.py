from playwright.sync_api import Page
from utils.constants import BASE_URL, TIMEOUT
from bs4 import BeautifulSoup

class HomePage:
    PRODUCT_NAME = "iPhone"
    
    def __init__(self, page: Page):
        self.page = page
        self.open()

    def open(self):
        self.page.goto(BASE_URL)

    def search_product(self):
        self.page.fill("input[name='search']", self.PRODUCT_NAME)
        self.page.click("button[type='button'][class='btn btn-default btn-lg']")

    def select_product(self):
        self.page.click(f"a:has-text('{self.PRODUCT_NAME}')")

    def go_to_cart(self):
        self.page.click("a[href$='route=checkout/cart']")

    def go_to_register_page(self):
        self.page.click("a[title='My Account']")
        self.page.wait_for_selector("a[href$='route=account/register']", timeout=TIMEOUT)
        self.page.click("a[href$='route=account/register']")

    def go_to_login_page(self):
        self.page.click("a[title='My Account']")
        self.page.wait_for_selector("a[href$='route=account/login']", timeout=TIMEOUT)
        self.page.click("a[href$='route=account/login']")

    def is_home_page_visible(self):
        logo_visible = self.page.is_visible("div#logo")
        content_visible = self.page.is_visible("div#content")
        return logo_visible and content_visible

    def is_product_search_successful(self):
        return self.page.is_visible(f"text=Search - {self.PRODUCT_NAME}")

    def get_all_links(self):
        html_content = self.page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return [link if link.startswith(BASE_URL) else f"{BASE_URL}{link}" for link in links]

    def open_link(self, link):
        self.page.goto(link)

    def is_page_loaded(self):
        return self.page.is_visible("body")
