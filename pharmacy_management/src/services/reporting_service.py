import sqlite3
import logging
import csv
from datetime import date
from src.utils.database import get_db_connection
from src.models.sale import Sale, SaleItem

def get_sales_by_user(user_id: int):
    """Retrieves all sales made by a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM sales WHERE user_id = ?", (user_id,))
        sales_data = cursor.fetchall()

        sales = []
        for sale_data in sales_data:
            sale_id = sale_data['id']
            cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
            items_data = cursor.fetchall()
            items = [SaleItem(medicine_id=item['medicine_id'], quantity=item['quantity']) for item in items_data]

            sales.append(Sale(
                id=sale_id,
                timestamp=date.fromisoformat(sale_data['timestamp'].split('T')[0]),
                user_id=sale_data['user_id'],
                items=items
            ))

        return sales
    except sqlite3.Error as e:
        logging.error(f"Error getting sales for user ID {user_id}: {e}")
        return []
    finally:
        conn.close()

def get_inventory_value():
    """Calculates the total value of the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(price * quantity) as total_value FROM medicines")
        result = cursor.fetchone()
        return result['total_value'] if result['total_value'] else 0
    except sqlite3.Error as e:
        logging.error(f"Error calculating inventory value: {e}")
        return 0
    finally:
        conn.close()

def get_sales_by_date_range(start_date: date, end_date: date):
    """Retrieves all sales within a given date range."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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
                timestamp=date.fromisoformat(sale_data['timestamp'].split('T')[0]),
                user_id=sale_data['user_id'],
                items=items
            ))

        return sales
    except sqlite3.Error as e:
        logging.error(f"Error getting sales for date range {start_date} to {end_date}: {e}")
        return []
    finally:
        conn.close()

def export_sales_to_csv(sales: list, filename: str):
    """Exports a list of sales to a CSV file."""
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['sale_id', 'timestamp', 'user_id', 'medicine_id', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for sale in sales:
                for item in sale.items:
                    writer.writerow({
                        'sale_id': sale.id,
                        'timestamp': sale.timestamp,
                        'user_id': sale.user_id,
                        'medicine_id': item.medicine_id,
                        'quantity': item.quantity
                    })
        logging.info(f"Sales data exported to {filename}")
        return True
    except IOError as e:
        logging.error(f"Error exporting sales to CSV: {e}")
        return False

# TODO: Implement the following functions:
# def get_expiring_medicines_report(): # This is already in inventory_service, maybe move or call from here
