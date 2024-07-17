from .base_page import BasePage

class HomePage(BasePage):
    def go_to_register_page(self):
        # 'My Account'ドロップダウンメニューをクリックして展開
        self.page.wait_for_selector("a[href$='route=account/account']", state='visible')
        self.click("a[href$='route=account/account']")
        
        # 登録リンクが表示されるのを待つ
        self.page.wait_for_selector("a[href$='route=account/register']", state='visible')
        self.click("a[href$='route=account/register']")

    def go_to_login_page(self):
        # 'My Account'ドロップダウンメニューをクリックして展開
        self.page.wait_for_selector("a[href$='route=account/account']", state='visible')
        self.click("a[href$='route=account/account']")

        # ログインリンクが表示されるのを待つ
        self.page.wait_for_selector("a[href$='route=account/login']", state='visible')
        self.click("a[href$='route=account/login']")

    def search_product(self, product_name: str):
        self.page.wait_for_selector("input[name='search']", state='visible')
        self.fill("input[name='search']", product_name)
        self.click("button[class='btn btn-default btn-lg']")

    def is_home_page_visible(self):
        # ホームページのタイトルが "Your Store" であることを確認
        return self.page.title() == "Your Store"
