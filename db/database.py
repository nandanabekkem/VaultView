import sqlite3  # Python's built-in library to work with SQLite databases - no install needed!

DB_PATH = "db/expense_tracker.db"  # The path where our database file will be created and stored

def get_connection():
    # Creates and returns a connection to the database
    # Think of this like "opening" the database file to work with it
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = get_connection()  # Open the database
    cursor = conn.cursor()   # Cursor is like a pen - we use it to write/read from the database

    # --- USERS TABLE ---
    # Stores login info for each user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each user, auto increases
            username TEXT UNIQUE NOT NULL,          -- Username, must be unique
            password TEXT NOT NULL                  -- Hashed password (never plain text!)
        )
    """)

    # --- TRANSACTIONS TABLE ---
    # Stores every income or expense entry
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique ID for each transaction
            user_id INTEGER NOT NULL,               -- Links transaction to a specific user
            type TEXT NOT NULL,                     -- 'income' or 'expense'
            category TEXT NOT NULL,                 -- e.g. Food, Savings, Investment
            amount REAL NOT NULL,                   -- The money amount (REAL = decimal numbers)
            note TEXT,                              -- Optional note the user can add
            date TEXT NOT NULL,                     -- Date of transaction stored as text (YYYY-MM-DD)
            FOREIGN KEY (user_id) REFERENCES users(id)  -- Links to users table
        )
    """)

    conn.commit()  # commit = "save" all the changes to the database
    conn.close()   # Always close the connection when done - like closing a file