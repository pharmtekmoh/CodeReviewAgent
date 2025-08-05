import sqlite3
import configparser
import os

# The root directory of the project, which is 'pharmacy_management'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_db_connection():
    """Establishes a connection to the database."""
    config = configparser.ConfigParser()
    config_path = os.path.join(BASE_DIR, 'config.ini')
    config.read(config_path)

    db_path_relative = config['Database']['path']
    db_path_absolute = os.path.join(BASE_DIR, db_path_relative)

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(db_path_absolute), exist_ok=True)

    conn = sqlite3.connect(db_path_absolute)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates all the necessary tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)

    # Patient table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        phone TEXT
    );
    """)

    # Supplier table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        address TEXT
    );
    """)

    # Medicine table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manufacturer TEXT,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        expiry_date TEXT NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
    );
    """)

    # Sales table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # Sale items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        medicine_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id),
        FOREIGN KEY (medicine_id) REFERENCES medicines (id)
    );
    """)

    # Prescription table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_name TEXT NOT NULL,
        medicine_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        prescription_date TEXT NOT NULL,
        filled INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (medicine_id) REFERENCES medicines (id)
    );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == '__main__':
    create_tables()
