import time
import requests
from functools import wraps


def retry_on_429(max_attempts=3, wait_seconds=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_attempts - 1:
                        print(f"429. waiting {wait_seconds}s, attempt {attempt + 1}")
                        time.sleep(wait_seconds)
                    else:
                        raise
            return None
        return wrapper
    return decorator