import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          
            database="healthcare_db"
        )

        if connection.is_connected():
            print("Connected to MySQL Database Successfully.")
            return connection

    except Error as e:
        print(f"Database Connection Error:\n{e}")
        return None


def close_connection(connection):
    """
    Closes the database connection.
    """
    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    conn = get_connection()

    if conn:
        print("Database connection test successful.")
        close_connection(conn)
    else:
        print("Unable to connect to the database.")