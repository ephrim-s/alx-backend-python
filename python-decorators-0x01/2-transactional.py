import sqlite3
import functools


# Reuse previous decorator: Handles opening & closing the connection
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


# New decorator: Handles transaction commit/rollback
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[INFO] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print("[ERROR] Transaction rolled back.")
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Update user's email with automatic connection and transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
