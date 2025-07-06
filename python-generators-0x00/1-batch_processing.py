import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:  # Yield the final remaining rows if any
            yield batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")
        return

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):          # Loop 1
        for user in batch:                                     # Loop 2
            if user['age'] > 25:                               # Conditional filtering
                yield user                                     # Yield matching user
