import sqlite3
import hashlib
import logging
from ..utils.database import get_db_connection
from ..models.user import User

def create_user(username, password, role):
    """Creates a new user with a hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        logging.info(f"User '{username}' created successfully with ID: {user_id}")
        return User(id=user_id, username=username, password_hash=password_hash, role=role)
    except sqlite3.IntegrityError:
        logging.warning(f"Failed to create user. Username '{username}' already exists.")
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    """Retrieves a user by their username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'], role=user_data['role'])
    return None

def check_user(username, password):
    """Checks a user's credentials."""
    user = get_user_by_username(username)
    if user:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user.password_hash == password_hash:
            logging.info(f"User '{username}' authenticated successfully.")
            return user
    return None
