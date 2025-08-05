import sqlite3
import logging
from datetime import datetime
from typing import List
from ..utils.database import get_db_connection
from ..models.sale import Sale, SaleItem

def create_sale(user_id: int, items: List[SaleItem]):
    """Creates a new sale, updating inventory in a single transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION;")

        # Create a new sale record
        now = datetime.now()
        cursor.execute(
            "INSERT INTO sales (timestamp, user_id) VALUES (?, ?)",
            (now.isoformat(), user_id)
        )
        sale_id = cursor.lastrowid

        total_price = 0

        for item in items:
            # Get the current medicine details
            cursor.execute("SELECT price, quantity FROM medicines WHERE id = ?", (item.medicine_id,))
            medicine_data = cursor.fetchone()

            if not medicine_data:
                raise ValueError(f"Medicine with ID {item.medicine_id} not found.")

            current_price = medicine_data['price']
            current_quantity = medicine_data['quantity']

            if current_quantity < item.quantity:
                raise ValueError(f"Not enough stock for medicine ID {item.medicine_id}.")

            # Insert into sale_items
            cursor.execute(
                "INSERT INTO sale_items (sale_id, medicine_id, quantity) VALUES (?, ?, ?)",
                (sale_id, item.medicine_id, item.quantity)
            )

            # Update medicine quantity
            new_quantity = current_quantity - item.quantity
            cursor.execute(
                "UPDATE medicines SET quantity = ? WHERE id = ?",
                (new_quantity, item.medicine_id)
            )

            total_price += current_price * item.quantity

        # Commit the transaction
        conn.commit()
        logging.info(f"Sale with ID {sale_id} created successfully by user ID {user_id}.")
        return Sale(id=sale_id, timestamp=now, user_id=user_id, items=items)

    except (sqlite3.Error, ValueError) as e:
        # Rollback in case of error
        conn.rollback()
        logging.error(f"Error creating sale for user ID {user_id}: {e}")
        return None
    finally:
        conn.close()

from datetime import date

def get_sale_by_id(sale_id: int):
    """Retrieves a single sale by its ID, including its items."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
    sale_data = cursor.fetchone()

    if not sale_data:
        conn.close()
        return None

    cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
    items_data = cursor.fetchall()

    conn.close()

    items = [SaleItem(medicine_id=item['medicine_id'], quantity=item['quantity']) for item in items_data]

    return Sale(
        id=sale_data['id'],
        timestamp=datetime.fromisoformat(sale_data['timestamp']),
        user_id=sale_data['user_id'],
        items=items
    )

def get_all_sales():
    """Retrieves all sales, including their items."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales")
    sales_data = cursor.fetchall()

    sales = []
    for sale_data in sales_data:
        sale_id = sale_data['id']
        cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
        items_data = cursor.fetchall()
        items = [SaleItem(medicine_id=item['medicine_id'], quantity=item['quantity']) for item in items_data]

        sales.append(Sale(
            id=sale_id,
            timestamp=datetime.fromisoformat(sale_data['timestamp']),
            user_id=sale_data['user_id'],
            items=items
        ))

    conn.close()
    return sales

def get_sales_by_date_range(start_date: date, end_date: date):
    """Retrieves all sales within a given date range."""
    conn = get_db_connection()
    cursor = conn.cursor()

    start_str = start_date.isoformat()
    end_str = end_date.isoformat()

    cursor.execute("SELECT * FROM sales WHERE date(timestamp) BETWEEN ? AND ?", (start_str, end_str))
    sales_data = cursor.fetchall()

    sales = []
    for sale_data in sales_data:
        sale_id = sale_data['id']
        cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
        items_data = cursor.fetchall()
        items = [SaleItem(medicine_id=item['medicine_id'], quantity=item['quantity']) for item in items_data]

        sales.append(Sale(
            id=sale_id,
            timestamp=datetime.fromisoformat(sale_data['timestamp']),
            user_id=sale_data['user_id'],
            items=items
        ))

    conn.close()
    return sales
