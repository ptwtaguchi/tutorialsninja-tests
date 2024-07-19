import time
import uuid
from datetime import datetime
import functools

def log_execution_time(func):
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
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{current_time}_{uuid.uuid4()}@example.com"
