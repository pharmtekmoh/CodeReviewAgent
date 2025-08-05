import sqlite3
import logging
from src.utils.database import get_db_connection
from src.models.patient import Patient

def add_patient(name: str, address: str, phone: str):
    """Adds a new patient to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (name, address, phone) VALUES (?, ?, ?)",
            (name, address, phone)
        )
        conn.commit()
        patient_id = cursor.lastrowid
        logging.info(f"Patient '{name}' (ID: {patient_id}) added.")
        return Patient(id=patient_id, name=name, address=address, phone=phone)
    except sqlite3.Error as e:
        logging.error(f"Error adding patient '{name}': {e}")
        return None
    finally:
        conn.close()

def get_patient_by_id(patient_id: int):
    """Retrieves a patient by their ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()
    if patient_data:
        return Patient(
            id=patient_data['id'],
            name=patient_data['name'],
            address=patient_data['address'],
            phone=patient_data['phone']
        )
    return None

def get_all_patients(page: int = 1, page_size: int = 10):
    """Retrieves a paginated list of all patients from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM patients LIMIT ? OFFSET ?", (page_size, offset))
    patients_data = cursor.fetchall()
    conn.close()
    return [
        Patient(
            id=patient['id'],
            name=patient['name'],
            address=patient['address'],
            phone=patient['phone']
        ) for patient in patients_data
    ]

def get_total_patients_count():
    """Returns the total number of patients."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM patients")
    result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0

def update_patient_details(patient_id: int, address: str, phone: str):
    """Updates a patient's address and phone number."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE patients SET address = ?, phone = ? WHERE id = ?",
            (address, phone, patient_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Patient with ID {patient_id} updated.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error updating patient with ID {patient_id}: {e}")
        return False
    finally:
        conn.close()

def delete_patient(patient_id: int):
    """Deletes a patient from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Patient with ID {patient_id} deleted.")
            return True
        return False
    except sqlite3.Error as e:
        logging.error(f"Error deleting patient with ID {patient_id}: {e}")
        return False
    finally:
        conn.close()
