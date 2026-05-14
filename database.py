import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    This function creates and returns a connection to the MySQL database.
    We will use this every time we need to save or read data.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None