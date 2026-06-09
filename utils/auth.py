import bcrypt                        # Library for hashing passwords securely
import sqlite3                       # To talk to our database
from db.database import get_connection  # Importing our get_connection function from database.py

# ─────────────────────────────────────────
# 🔒 HASH PASSWORD
# ─────────────────────────────────────────
def hash_password(plain_password):
    # bcrypt needs the password as bytes, not a string
    # .encode("utf-8") converts string → bytes
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    # gensalt() generates a random "salt" - extra random data mixed into the hash
    # so even if two users have the same password, their hashes will be different!

# ─────────────────────────────────────────
# ✅ CHECK PASSWORD
# ─────────────────────────────────────────
def verify_password(plain_password, hashed_password):
    # Checks if the entered password matches the stored hash
    # Returns True if match, False if not
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

# ─────────────────────────────────────────
# 📝 SIGN UP
# ─────────────────────────────────────────
def signup_user(username, password):
    conn = get_connection()       # Open database
    cursor = conn.cursor()        # Get our "pen"

    try:
        hashed = hash_password(password)   # Hash the password before saving
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
            # (?, ?) are placeholders - prevents SQL injection attacks! 🔒
            # Never directly put user input into SQL strings
        )
        conn.commit()             # Save changes
        return True, "Account created successfully! 🎉"

    except sqlite3.IntegrityError:
        # This error fires when username already exists (because we set it as UNIQUE)
        return False, "Username already exists! Try another one."

    finally:
        conn.close()              # Always close, whether it worked or not

# ─────────────────────────────────────────
# 🔑 LOG IN
# ─────────────────────────────────────────
def login_user(username, password):
    conn = get_connection()       # Open database
    cursor = conn.cursor()        # Get our "pen"

    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)               # Comma makes it a tuple - required by sqlite3
    )
    user = cursor.fetchone()      # fetchone() gets the first matching row, or None if not found
    conn.close()

    if user is None:
        return False, None, "Username not found!"   # No such user

    user_id, hashed_password = user   # Unpack the row into two variables

    if verify_password(password, hashed_password):
        return True, user_id, "Login successful! 👋"
    else:
        return False, None, "Wrong password!"