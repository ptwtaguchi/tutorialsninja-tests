import time
import uuid
import os
import inspect
from datetime import datetime
import functools
from pathlib import Path
from playwright.sync_api import Page

def log_execution_time(func):
    """
    関数の実行時間をログ出力するデコレータ。
    """
    @functools.wraps(func)
    def wrapper(self, page, *args, **kwargs):
        start_time = time.time()
        print(f"Starting {func.__name__} at {datetime.now()}")
        result = func(self, page, *args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Finished {func.__name__} at {datetime.now()}, Execution time: {execution_time:.2f} seconds")
        return result
    return wrapper

def generate_unique_email():
    """
    現在の日時とUUIDを用いて一意のメールアドレスを生成する関数。
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{current_time}_{uuid.uuid4()}@example.com"

def take_screenshot(page: Page, name: str):
    """
    指定された名前でスクリーンショットを保存する関数。
    """
    screenshots_dir = "screenshots"
    Path(screenshots_dir).mkdir(parents=True, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, f"{name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def assert_with_screenshot(page: Page, condition: bool):
    """
    アサーションを行い、スクリーンショットを取得する関数。
    アサーションが失敗した場合にもスクリーンショットを保存する。
    """
    caller = inspect.stack()[1]
    module = inspect.getmodule(caller[0])
    module_name = os.path.splitext(os.path.basename(module.__file__))[0]
    screenshot_name = f"{module_name}_{caller.function}"
    
    take_screenshot(page, screenshot_name)
    assert condition
