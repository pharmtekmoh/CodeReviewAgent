import sqlite3
import logging
from src.utils.database import get_db_connection
from src.models.medicine import Medicine
from datetime import date

def add_medicine(name: str, manufacturer: str, price: float, quantity: int, expiry_date: date, supplier_id: int):
    """Adds a new medicine to the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO medicines (name, manufacturer, price, quantity, expiry_date, supplier_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, manufacturer, price, quantity, expiry_date.isoformat(), supplier_id)
        )
        conn.commit()
        medicine_id = cursor.lastrowid
        logging.info(f"Medicine '{name}' (ID: {medicine_id}) added to inventory.")
        return Medicine(id=medicine_id, name=name, manufacturer=manufacturer, price=price, quantity=quantity, expiry_date=expiry_date)
    except sqlite3.Error as e:
        logging.error(f"Error adding medicine '{name}': {e}")
        return None
    finally:
        conn.close()

def get_medicine_by_id(medicine_id: int):
    """Retrieves a medicine by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,))
    medicine_data = cursor.fetchone()
    conn.close()
    if medicine_data:
        return Medicine(
            id=medicine_data['id'],
            name=medicine_data['name'],
            manufacturer=medicine_data['manufacturer'],
            price=medicine_data['price'],
            quantity=medicine_data['quantity'],
            expiry_date=date.fromisoformat(medicine_data['expiry_date'])
        )
    return None

def get_all_medicines(page: int = 1, page_size: int = 10):
    """Retrieves a paginated list of all medicines from the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM medicines LIMIT ? OFFSET ?", (page_size, offset))
    medicines_data = cursor.fetchall()
    conn.close()
    return [
        Medicine(
            id=med['id'],
            name=med['name'],
            manufacturer=med['manufacturer'],
            price=med['price'],
            quantity=med['quantity'],
            expiry_date=date.fromisoformat(med['expiry_date'])
        ) for med in medicines_data
    ]

def get_total_medicines_count():
    """Returns the total number of medicines in the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM medicines")
    result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0

def update_medicine_details(medicine_id: int, price: float, quantity: int):
    """Updates a medicine's price and quantity."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE medicines SET price = ?, quantity = ? WHERE id = ?",
            (price, quantity, medicine_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Medicine with ID {medicine_id} updated.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error updating medicine with ID {medicine_id}: {e}")
        return False
    finally:
        conn.close()

def delete_medicine(medicine_id: int):
    """Deletes a medicine from the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Medicine with ID {medicine_id} deleted.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error deleting medicine with ID {medicine_id}: {e}")
        return False
    finally:
        conn.close()

from datetime import timedelta

def search_medicines(term: str):
    """Searches for medicines by name or manufacturer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        search_term = f"%{term}%"
        cursor.execute("SELECT * FROM medicines WHERE name LIKE ? OR manufacturer LIKE ?", (search_term, search_term))
        medicines_data = cursor.fetchall()
        return [
            Medicine(
                id=med['id'],
                name=med['name'],
                manufacturer=med['manufacturer'],
                price=med['price'],
                quantity=med['quantity'],
                expiry_date=date.fromisoformat(med['expiry_date'])
            ) for med in medicines_data
        ]
    except sqlite3.Error as e:
        logging.error(f"Error searching for medicines with term '{term}': {e}")
        return []
    finally:
        conn.close()

def get_low_stock_medicines(threshold: int):
    """Retrieves medicines with quantity below a given threshold."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE quantity < ?", (threshold,))
    medicines_data = cursor.fetchall()
    conn.close()
    return [
        Medicine(
            id=med['id'],
            name=med['name'],
            manufacturer=med['manufacturer'],
            price=med['price'],
            quantity=med['quantity'],
            expiry_date=date.fromisoformat(med['expiry_date'])
        ) for med in medicines_data
    ]

def get_expiring_medicines(days: int):
    """Retrieves medicines expiring within a given number of days."""
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()
    future_date = today + timedelta(days=days)

    cursor.execute("SELECT * FROM medicines WHERE expiry_date BETWEEN ? AND ?", (today.isoformat(), future_date.isoformat()))
    medicines_data = cursor.fetchall()
    conn.close()
    return [
        Medicine(
            id=med['id'],
            name=med['name'],
            manufacturer=med['manufacturer'],
            price=med['price'],
            quantity=med['quantity'],
            expiry_date=date.fromisoformat(med['expiry_date'])
        ) for med in medicines_data
    ]
