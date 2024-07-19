import pytest
from playwright.sync_api import sync_playwright
from utils.constants import BASE_URL, TIMEOUT, HEADLESS_MODE, CHROMIUM, FIREFOX, WEBKIT

def pytest_addoption(parser):
    """
    pytestのコマンドラインオプションを追加します。
    --playwright-headless: ヘッドレスモードをオンまたはオフに設定します。
    --playwright-browser: 使用するブラウザのタイプを設定します（chromium、firefox、webkit）。
    """
    parser.addoption("--playwright-headless", action="store", default="on" if HEADLESS_MODE else "off", help="Headless mode: 'on' or 'off'")
    parser.addoption("--playwright-browser", action="store", default="chromium", help="Browser type: 'chromium', 'firefox', or 'webkit'")

@pytest.fixture(scope="session")
def browser_instance(pytestconfig):
    """
    指定されたオプションに基づいてPlaywrightのブラウザインスタンスを作成します。
    テストセッション全体で共有されるブラウザインスタンスを提供します。
    """
    headless_option = pytestconfig.getoption("--playwright-headless")
    headless = headless_option == "on"
    browser_type = pytestconfig.getoption("--playwright-browser")

    with sync_playwright() as p:
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError("Invalid browser type specified")

        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser_instance):
    """
    各テスト関数のために新しいブラウザページを作成し、提供します。
    テスト関数が終了するとページを閉じます。
    """
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    テストの実行結果を処理し、テストが失敗した場合にスクリーンショットを取得します。
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs['page']
        module_name = item.module.__name__
        test_name = item.name
        screenshot_name = f"{module_name}_{test_name}"
        from utils.helpers import take_screenshot
        take_screenshot(page, screenshot_name)
