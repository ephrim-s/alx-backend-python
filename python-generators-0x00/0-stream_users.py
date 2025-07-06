import mysql.connector
from mysql.connector import Error

def stream_users():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")
        return
