import sqlite3
import logging
from src.utils.database import get_db_connection
from src.models.supplier import Supplier

def add_supplier(name: str, contact_person: str, phone: str, address: str):
    """Adds a new supplier to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO suppliers (name, contact_person, phone, address) VALUES (?, ?, ?, ?)",
            (name, contact_person, phone, address)
        )
        conn.commit()
        supplier_id = cursor.lastrowid
        logging.info(f"Supplier '{name}' (ID: {supplier_id}) added.")
        return Supplier(id=supplier_id, name=name, contact_person=contact_person, phone=phone, address=address)
    except sqlite3.Error as e:
        logging.error(f"Error adding supplier '{name}': {e}")
        return None
    finally:
        conn.close()

def get_supplier_by_id(supplier_id: int):
    """Retrieves a supplier by their ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
    supplier_data = cursor.fetchone()
    conn.close()
    if supplier_data:
        return Supplier(
            id=supplier_data['id'],
            name=supplier_data['name'],
            contact_person=supplier_data['contact_person'],
            phone=supplier_data['phone'],
            address=supplier_data['address']
        )
    return None

def get_all_suppliers(page: int = 1, page_size: int = 10):
    """Retrieves a paginated list of all suppliers from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM suppliers LIMIT ? OFFSET ?", (page_size, offset))
    suppliers_data = cursor.fetchall()
    conn.close()
    return [
        Supplier(
            id=supplier['id'],
            name=supplier['name'],
            contact_person=supplier['contact_person'],
            phone=supplier['phone'],
            address=supplier['address']
        ) for supplier in suppliers_data
    ]

def get_total_suppliers_count():
    """Returns the total number of suppliers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM suppliers")
    result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0

def update_supplier_details(supplier_id: int, contact_person: str, phone: str, address: str):
    """Updates a supplier's details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE suppliers SET contact_person = ?, phone = ?, address = ? WHERE id = ?",
            (contact_person, phone, address, supplier_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Supplier with ID {supplier_id} updated.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error updating supplier with ID {supplier_id}: {e}")
        return False
    finally:
        conn.close()

def delete_supplier(supplier_id: int):
    """Deletes a supplier from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Supplier with ID {supplier_id} deleted.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error deleting supplier with ID {supplier_id}: {e}")
        return False
    finally:
        conn.close()
