from playwright.sync_api import Page
from utils.constants import TIMEOUT
import time

class ProductPage:
    def __init__(self, page: Page):
        self.page = page

    def add_to_cart(self):
        # カートに追加ボタンをクリックする処理だが、テストがよく失敗したため、
        # 動作が安定するように処理を追記している

        # カートに追加ボタンが表示されるのを待つ
        print("Waiting for add to cart button to be visible...")
        self.page.wait_for_selector("button#button-cart", timeout=TIMEOUT)
        
        # ボタンが表示されている状態のスクリーンショットを取得
        self.page.screenshot(path='screenshots/product_page_01_before_click_add_to_cart.png')
        
        # カートに追加ボタンがクリック可能になるのを待つ
        print("Waiting for add to cart button to be enabled...")
        button_clicked = False
        for i in range(5):  # 最大5回リトライする
            try:
                button = self.page.query_selector("button#button-cart:enabled")
                if button:
                    print(f"Attempting to click add to cart button, attempt {i+1}")
                    self.page.evaluate("document.querySelector('button#button-cart').click()")
                    button_clicked = True
                    break
            except Exception as e:
                print(f"Attempt {i+1} failed: {e}")
                time.sleep(3)  # 3秒待ってから再試行
    
        if not button_clicked:
            raise Exception("Failed to click add to cart button")
        
        # ボタンがクリックされた後のスクリーンショットを取得
        self.page.screenshot(path='screenshots/product_page_02_after_click_add_to_cart.png')
        
        # カートに追加ボタンがクリックされた後、ページの読み込みを待つ
        print("Waiting for network to be idle...")
        self.page.wait_for_load_state('networkidle', timeout=TIMEOUT * 3)  # タイムアウトを3倍に増やす

        print("Waiting for page to be fully loaded...")
        self.page.wait_for_load_state('load', timeout=TIMEOUT * 3)  # タイムアウトを3倍に増やす
        
        # 成功メッセージが表示される前のスクリーンショットを取得
        self.page.screenshot(path='screenshots/product_page_03_before_check_success_message.png')
        
        # 成功メッセージが表示されるのを確認する
        print("Waiting for success message to be visible...")
        success_message_visible = False
        for i in range(5):  # 最大5回リトライする
            try:
                self.page.wait_for_selector("div.alert-success", timeout=TIMEOUT)  # タイムアウトを増やす
                if self.page.is_visible("div.alert-success"):
                    print("Success message is visible.")
                    success_message_visible = True
                    break
            except Exception as e:
                print(f"Attempt {i+1} to find success message failed: {e}")
                time.sleep(3)  # 3秒待ってから再試行

        if not success_message_visible:
            # 状態の確認
            print("Retrying to find success message after network idle...")
            self.page.wait_for_load_state('networkidle', timeout=TIMEOUT * 3)  # タイムアウトを増やす
            for i in range(5):  # 最大5回リトライする
                try:
                    self.page.wait_for_selector("div.alert-success", timeout=TIMEOUT)  # タイムアウトを増やす
                    if self.page.is_visible("div.alert-success"):
                        print("Success message is visible.")
                        success_message_visible = True
                        break
                except Exception as e:
                    print(f"Retry attempt {i+1} to find success message failed: {e}")
                    time.sleep(3)  # 3秒待ってから再試行
    
        if not success_message_visible:
            print("Current page URL:", self.page.url)
            print("Page content:", self.page.content())
            print("JavaScript Errors:", self.page.evaluate("window.onerror"))
            raise Exception("Add to cart success message not visible")

    def is_product_added_to_cart(self):
        return self.page.is_visible("div.alert-success")
