import time
import sqlite3
import functools


# Reuse from Task 1: Automatic connection handling
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Task 3: Retry on failure decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[INFO] Attempt {attempt}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[WARNING] Attempt {attempt} failed: {e}")
                    last_exception = e
                    time.sleep(delay)
            print("[ERROR] All retries failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
