import pytest
import uuid
from datetime import datetime
from pages.home_page import HomePage
from pages.account_page import AccountPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BASE_URL = "https://tutorialsninja.com/demo/"

@pytest.fixture(scope="session")
def browser_context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

def generate_unique_email():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{current_time}_{uuid.uuid4()}@example.com"

def logout(page):
    try:
        page.goto("https://tutorialsninja.com/demo/index.php?route=account/logout")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
    except Exception:
        pass

def clear_cart(page):
    page.goto("https://tutorialsninja.com/demo/index.php?route=checkout/cart")
    page.wait_for_selector("div#content h1:has-text('Shopping Cart')")
    remove_buttons = page.locator("button[data-original-title='Remove']").all()
    for button in remove_buttons:
        button.click()
    page.wait_for_timeout(1000)  # Wait for 1 second to ensure cart is cleared

@pytest.mark.usefixtures("page")
class TestHomePage:
    def test_home_page_display(self, page):
        home_page = HomePage(page)
        home_page.open()
        assert home_page.is_home_page_visible()
        logout(page)

@pytest.mark.usefixtures("page")
class TestUserRegistration:
    def test_user_registration(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)

        home_page.open()

        # ページの完全読み込みを待機
        page.wait_for_load_state('load')
        page.wait_for_load_state('networkidle')

        # My Accountドロップダウンメニューを開く
        page.click("a[href$='account/account']")

        # Registerページリンクの表示を待つ
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=60000)

        home_page.go_to_register_page()

        unique_email = generate_unique_email()
        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        # アカウント作成の確認メッセージが表示されるまで待機
        page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')", timeout=60000)
        assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")

        logout(page)

@pytest.mark.usefixtures("page")
class TestUserLoginLogout:
    def test_user_login_logout(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)

        home_page.open()

        unique_email = generate_unique_email()

        # My Accountドロップダウンメニューを開く
        page.click("a[href$='account/account']")
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=60000)

        home_page.go_to_register_page()

        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        # アカウント作成の確認メッセージが表示されるまで待機
        page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')", timeout=60000)
        assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")

        # Continueボタンをクリックしてマイアカウントページに遷移
        page.click("div.buttons a.btn.btn-primary")
        page.wait_for_selector("div#content h2:has-text('My Account')")

        # 画面下部にスクロール
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # ログアウトリンクをクリックする前に表示されるまで待機
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=60000)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")

        # 一定時間待つ
        # page.wait_for_timeout(5000)

        # サイドバーのログインリンクを待機してクリック
        try:
            sidebar_login = page.locator("aside#column-right a[href$='route=account/login']:visible").first
            sidebar_login.wait_for(timeout=60000)
            sidebar_login.click()
        except Exception as e:
            print(f"Sidebar login error: {e}")
            raise

        page.wait_for_selector("h2:has-text('Returning Customer')")
        account_page.login(unique_email, "password")
        page.wait_for_selector("div#content h2:has-text('My Account')")
        assert "My Account" in account_page.get_text("div#content h2")

        # 再度ログアウト
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=60000)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")

        logout(page)

@pytest.mark.usefixtures("page")
class TestPasswordReset:
    def test_password_reset(self, page):
        home_page = HomePage(page)
        account_page = AccountPage(page)

        home_page.open()

        unique_email = generate_unique_email()

        # My Accountドロップダウンメニューを開く
        page.click("a[href$='account/account']")
        page.wait_for_selector("a[href$='route=account/register']:visible", timeout=60000)

        # アカウント登録ページへ遷移
        home_page.go_to_register_page()

        # ユーザーを登録
        account_page.register_user("Test", "User", unique_email, "123456789", "password")

        # 登録後ログアウト
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=60000)
        page.click("a[href$='route=account/logout']:visible")
        page.wait_for_selector("div#content h1:has-text('Account Logout')")
        assert "Account Logout" in account_page.get_text("div#content h1")

        # ログインページに遷移
        page.goto("https://tutorialsninja.com/demo/index.php?route=account/login")
        page.wait_for_selector("a[href$='route=account/forgotten']", timeout=60000)

        # Forgotten Passwordのリンクをクリック
        page.click("a[href$='route=account/forgotten']")
        page.wait_for_selector("input[name='email']", timeout=60000)

        # メールアドレスを入力してContinueボタンをクリック
        page.fill("input[name='email']", unique_email)
        page.click("input[type='submit']")

        # 確認メッセージが表示されることを確認
        page.wait_for_selector("div.alert.alert-success.alert-dismissible:has-text('An email with a confirmation link has been sent your email address.')", timeout=60000)
        assert "An email with a confirmation link has been sent your email address." in account_page.get_text("div.alert.alert-success.alert-dismissible")

        logout(page)

@pytest.mark.usefixtures("page")
class TestProductSearch:
    @pytest.mark.parametrize("product_name", ["iPhone"])
    def test_product_search(self, page, product_name):
        home_page = HomePage(page)
        home_page.open()
        home_page.search_product(product_name)
        assert home_page.is_product_search_successful(product_name)
        logout(page)

@pytest.mark.usefixtures("page")
class TestAddToCart:
    def test_add_to_cart(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        # ホームページを開く
        home_page.open()
    
        # ページの完全読み込みを待機
        page.wait_for_load_state('load')
        page.wait_for_load_state('networkidle')
        
        # 商品を検索する
        home_page.search_product("iPhone")
        
        # 検索結果から商品を選択する
        page.wait_for_selector(f"a:has-text('iPhone')", timeout=60000)
        home_page.select_product("iPhone")
    
        # 一定時間待つ
        page.wait_for_timeout(3000)

        # 商品をカートに追加する
        product_page.add_to_cart()

        # カートに商品が追加されたかを確認する
        added_to_cart = product_page.is_product_added_to_cart()

        # デバッグ出力
        if not added_to_cart:
            page.screenshot(path=f"screenshots/failed_add_to_cart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            print("Failed to add product to cart.")
        
        assert added_to_cart, "Product was not added to cart successfully."
        
        clear_cart(page)
        logout(page)

@pytest.mark.usefixtures("page")
class TestCheckoutProcess:
    def test_checkout_process(self, page):
        home_page = HomePage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)

        home_page.open()
    
        # ページの完全読み込みを待機
        page.wait_for_load_state('load')
        page.wait_for_load_state('networkidle')
        
        # 商品を検索する
        home_page.search_product("iPhone")

        # 検索結果から商品を選択する
        page.wait_for_selector(f"a:has-text('iPhone')", timeout=60000)
        home_page.select_product("iPhone")

        # 一定時間待つ
        page.wait_for_timeout(3000)

        # 商品をカートに追加する
        product_page.add_to_cart()

        # カートに商品が追加されたかを確認する
        added_to_cart = product_page.is_product_added_to_cart()

        # デバッグ出力
        if not added_to_cart:
            page.screenshot(path=f"screenshots/failed_add_to_cart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            print("Failed to add product to cart.")
        
        assert added_to_cart, "Product was not added to cart successfully."

        home_page.go_to_cart()
        assert cart_page.is_stock_unavailable()

        clear_cart(page)
        logout(page)

@pytest.mark.usefixtures("page")
class TestNavigationAndPages:
    def test_navigation_and_pages(self, page):
        home_page = HomePage(page)

        home_page.open()
        links = home_page.get_all_links()

        for link in links:
            home_page.open_link(link)
            assert home_page.is_page_loaded()

        logout(page)
