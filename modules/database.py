import sqlite3
from sqlite3 import Error
import os

# Database path relative to the project directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

# Create a connection to the SQLite database
def create_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Create tables
def create_tables():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            email TEXT NOT NULL,
                            password TEXT NOT NULL
                        )''')
        conn.commit()
        conn.close()



# Fetch all users from the database
def fetch_all_users():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Initialize the database by creating tables and inserting sample data
def init_db():
    create_tables()

# Call this function to initialize the database
init_db()
