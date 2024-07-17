import pytest
import uuid
from datetime import datetime
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.account_page import AccountPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from bs4 import BeautifulSoup

BASE_URL = "https://tutorialsninja.com/demo/"

@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()

def generate_unique_email():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{current_time}_{uuid.uuid4()}@example.com"

def test_home_page_display(page):
    home_page = HomePage(page)
    home_page.goto(BASE_URL)
    assert home_page.is_home_page_visible()

def test_user_registration(page):
    home_page = HomePage(page)
    account_page = AccountPage(page)

    home_page.goto(BASE_URL)
    home_page.go_to_register_page()
    unique_email = generate_unique_email()
    account_page.register_user("Test", "User", unique_email, "123456789", "password")
    
    # アカウント作成の確認メッセージが表示されるまで待機
    page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')")
    assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")

def test_user_login_logout(page):
    home_page = HomePage(page)
    account_page = AccountPage(page)

    home_page.goto(BASE_URL)

    # まずユーザーを登録
    home_page.go_to_register_page()
    unique_email = generate_unique_email()
    account_page.register_user("Test", "User", unique_email, "123456789", "password")
    
    # アカウント作成の確認メッセージが表示されるまで待機
    page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')")
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

    # ログインページに遷移
    home_page.go_to_login_page()
    account_page.login(unique_email, "password")
    page.wait_for_selector("div#content h2:has-text('My Account')")
    assert "My Account" in account_page.get_text("div#content h2")

    # 再度ログアウト
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=60000)
    page.click("a[href$='route=account/logout']:visible")
    page.wait_for_selector("div#content h1:has-text('Account Logout')")
    assert "Account Logout" in account_page.get_text("div#content h1")

def test_password_reset(page):
    home_page = HomePage(page)
    account_page = AccountPage(page)

    home_page.goto(BASE_URL)

    # まずユーザーを登録
    home_page.go_to_register_page()
    unique_email = generate_unique_email()
    account_page.register_user("Test", "User", unique_email, "123456789", "password")

    # アカウント作成の確認メッセージが表示されるまで待機
    page.wait_for_selector("div#content h1:has-text('Your Account Has Been Created!')")
    assert "Your Account Has Been Created!" in account_page.get_text("div#content h1")

    # Continueボタンをクリックしてマイアカウントページに遷移
    page.click("div.buttons a.btn.btn-primary")
    page.wait_for_selector("div#content h2:has-text('My Account')")

    # ログアウト
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_selector("a[href$='route=account/logout']:visible", timeout=60000)
    page.click("a[href$='route=account/logout']:visible")
    page.wait_for_selector("div#content h1:has-text('Account Logout')")
    assert "Account Logout" in account_page.get_text("div#content h1")

    # パスワードリセットを行う
    home_page.go_to_login_page()
    page.click("a:has-text('Forgotten Password')")
    account_page.reset_password(unique_email)
    
    # ログを追加して、ページのコンテンツを確認
    print(page.content())
    
    assert "An email with a confirmation link has been sent your email address." in account_page.get_text("body")

def test_product_search(page):
    home_page = HomePage(page)

    home_page.goto(BASE_URL)
    home_page.search_product("iPhone")
    assert "Search - iPhone" in home_page.get_text("body")
    assert "iPhone" in home_page.get_text("body")

def test_add_to_cart(page):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    home_page.goto(BASE_URL)
    home_page.search_product("iPhone")
    page.wait_for_selector("a:has-text('iPhone')")
    page.click("a:has-text('iPhone')")
    
    product_page.add_to_cart()

    # Successメッセージが表示されるまで待機
    page.wait_for_selector("div.alert-success", timeout=10000)
    
    # メッセージを取得して確認
    success_message = product_page.get_text("div.alert-success")
    assert "Success: You have added" in success_message

    # カートページに移動して確認
    page.click("a[href$='route=checkout/cart']")
    page.wait_for_selector("div#content h1:has-text('Shopping Cart')")
    assert "Shopping Cart" in cart_page.get_text("div#content h1")

def test_checkout_process(page):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.goto(BASE_URL)
    home_page.search_product("iPhone")
    home_page.click("a:has-text('iPhone')")
    product_page.add_to_cart()
    home_page.click("a[href$='route=checkout/cart']")
    assert page.is_visible("text=Products marked with *** are not available in the desired quantity or not in stock!")

def test_navigation_and_pages(page):
    home_page = HomePage(page)

    home_page.goto(BASE_URL)
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 全てのリンクを収集
    links = [a['href'] for a in soup.find_all('a', href=True)]

    for link in links:
        if link.startswith(BASE_URL) or link.startswith('/'):
            full_link = link if link.startswith(BASE_URL) else BASE_URL + link
            home_page.goto(full_link)
            assert home_page.is_visible("body")
