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
        
        # Users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')

        # Servers (or guilds) table
        cursor.execute('''CREATE TABLE IF NOT EXISTS servers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            owner_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (owner_id) REFERENCES users (id)
                        )''')

        # Server memberships table
        cursor.execute('''CREATE TABLE IF NOT EXISTS server_memberships (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            server_id INTEGER NOT NULL,
                            role TEXT DEFAULT 'member',
                            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (server_id) REFERENCES servers (id)
                        )''')

        # Channels table
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            server_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (server_id) REFERENCES servers (id)
                        )''')

        # Messages table
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT NOT NULL,
                            user_id INTEGER NOT NULL,
                            channel_id INTEGER NOT NULL,
                            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (channel_id) REFERENCES channels (id)
                        )''')

        # Friendships table
        cursor.execute('''CREATE TABLE IF NOT EXISTS friendships (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id1 INTEGER NOT NULL,
                            user_id2 INTEGER NOT NULL,
                            status TEXT CHECK(status IN ('pending', 'accepted', 'blocked')) DEFAULT 'pending',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id1) REFERENCES users (id),
                            FOREIGN KEY (user_id2) REFERENCES users (id)
                        )''')

        conn.commit()
        conn.close()
        print("Tables created successfully.")




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
