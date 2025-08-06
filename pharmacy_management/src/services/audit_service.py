import sqlite3
import logging
from datetime import datetime
from src.utils.database import get_db_connection

def log_action(user_id: int, action: str):
    """Logs an action to the audit log."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO audit_log (user_id, action, timestamp) VALUES (?, ?, ?)",
            (user_id, action, timestamp)
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error logging action for user ID {user_id}: {e}")
    finally:
        conn.close()
