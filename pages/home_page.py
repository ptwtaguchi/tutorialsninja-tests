from playwright.sync_api import Page
from bs4 import BeautifulSoup

class HomePage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("https://tutorialsninja.com/demo/")

    def search_product(self, product_name):
        self.page.fill("input[name='search']", product_name)
        self.page.click("button[type='button'][class='btn btn-default btn-lg']")

    def select_product(self, product_name):
        self.page.click(f"a:has-text('{product_name}')")

    def go_to_cart(self):
        self.page.click("a[href$='route=checkout/cart']")

    def go_to_register_page(self):
        self.page.click("a[href$='route=account/register']")

    def go_to_login_page(self):
        self.page.click("a[href$='route=account/login']")

    def is_home_page_visible(self):
        logo_visible = self.page.is_visible("div#logo")
        content_visible = self.page.is_visible("div#content")
        
        # デバッグ用ログ
        print(f"Logo visible: {logo_visible}")
        print(f"Content visible: {content_visible}")

        return logo_visible and content_visible

    def is_product_search_successful(self, product_name):
        return self.page.is_visible(f"text=Search - {product_name}")

    def get_all_links(self):
        html_content = self.page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return [link if link.startswith("https://tutorialsninja.com/demo/") else f"https://tutorialsninja.com/demo/{link}" for link in links]

    def open_link(self, link):
        self.page.goto(link)

    def is_page_loaded(self):
        return self.page.is_visible("body")
