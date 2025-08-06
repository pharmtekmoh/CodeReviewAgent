import sqlite3
import hashlib
import logging
from src.utils.database import get_db_connection
from src.models.user import User
from . import audit_service

def create_user(username, password, role_id):
    """Creates a new user with a hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role_id) VALUES (?, ?, ?)",
            (username, password_hash, role_id)
        )
        conn.commit()
        user_id = cursor.lastrowid
        logging.info(f"User '{username}' created successfully with ID: {user_id}")
        audit_service.log_action(user_id, f"Created user '{username}'")
        return User(id=user_id, username=username, password_hash=password_hash, role_id=role_id)
    except sqlite3.IntegrityError:
        logging.warning(f"Failed to create user. Username '{username}' already exists.")
        return None
    finally:
        conn.close()

def create_role(name: str):
    """Creates a new role."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO roles (name) VALUES (?)", (name,))
        conn.commit()
        role_id = cursor.lastrowid
        logging.info(f"Role '{name}' created with ID: {role_id}")
        audit_service.log_action(None, f"Created role '{name}'")
        return role_id
    except sqlite3.IntegrityError:
        logging.warning(f"Role '{name}' already exists.")
        return None
    finally:
        conn.close()

def create_permission(name: str):
    """Creates a new permission."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO permissions (name) VALUES (?)", (name,))
        conn.commit()
        permission_id = cursor.lastrowid
        logging.info(f"Permission '{name}' created with ID: {permission_id}")
        audit_service.log_action(None, f"Created permission '{name}'")
        return permission_id
    except sqlite3.IntegrityError:
        logging.warning(f"Permission '{name}' already exists.")
        return None
    finally:
        conn.close()

def assign_permission_to_role(role_id: int, permission_id: int):
    """Assigns a permission to a role."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (role_id, permission_id))
        conn.commit()
        logging.info(f"Permission {permission_id} assigned to role {role_id}")
        audit_service.log_action(None, f"Assigned permission {permission_id} to role {role_id}")
        return True
    except sqlite3.IntegrityError:
        logging.warning(f"Permission {permission_id} already assigned to role {role_id}")
        return False
    finally:
        conn.close()

def get_user_permissions(user_id: int):
    """Retrieves all permissions for a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        JOIN users u ON rp.role_id = u.role_id
        WHERE u.id = ?
    """, (user_id,))
    permissions = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return permissions

def get_all_roles():
    """Retrieves all roles from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    conn.close()
    return roles

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
