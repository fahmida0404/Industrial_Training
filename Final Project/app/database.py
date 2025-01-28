import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_db_connection():
    try:
        # print("Initializing MySql connection")
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        
        # print("MySQL Database connection successful")
        return connection
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None
