import sqlite3
import logging
from datetime import date
from src.utils.database import get_db_connection
from src.models.prescription import Prescription

def create_prescription(patient_id: int, doctor_name: str, medicine_id: int, quantity: int, prescription_date: date):
    """Creates a new prescription."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO prescriptions (patient_id, doctor_name, medicine_id, quantity, prescription_date) VALUES (?, ?, ?, ?, ?)",
            (patient_id, doctor_name, medicine_id, quantity, prescription_date.isoformat())
        )
        conn.commit()
        prescription_id = cursor.lastrowid
        logging.info(f"Prescription for patient ID {patient_id} created with ID: {prescription_id}")
        return Prescription(id=prescription_id, patient_id=patient_id, doctor_name=doctor_name, medicine_id=medicine_id, quantity=quantity, prescription_date=prescription_date, filled=False)
    except sqlite3.Error as e:
        logging.error(f"Error creating prescription for patient ID {patient_id}: {e}")
        return None
    finally:
        conn.close()

def get_prescription_by_id(prescription_id: int):
    """Retrieves a prescription by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescriptions WHERE id = ?", (prescription_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return Prescription(
            id=data['id'],
            patient_id=data['patient_id'],
            doctor_name=data['doctor_name'],
            medicine_id=data['medicine_id'],
            quantity=data['quantity'],
            prescription_date=date.fromisoformat(data['prescription_date']),
            filled=bool(data['filled'])
        )
    return None

def get_prescriptions_by_patient(patient_id: int):
    """Retrieves all prescriptions for a specific patient."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescriptions WHERE patient_id = ?", (patient_id,))
    data_list = cursor.fetchall()
    conn.close()
    return [
        Prescription(
            id=data['id'],
            patient_id=data['patient_id'],
            doctor_name=data['doctor_name'],
            medicine_id=data['medicine_id'],
            quantity=data['quantity'],
            prescription_date=date.fromisoformat(data['prescription_date']),
            filled=bool(data['filled'])
        ) for data in data_list
    ]

def fill_prescription(prescription_id: int):
    """Marks a prescription as filled and updates inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION;")

        prescription = get_prescription_by_id(prescription_id)
        if not prescription:
            raise ValueError("Prescription not found.")
        if prescription.filled:
            raise ValueError("Prescription already filled.")

        # Check stock
        cursor.execute("SELECT quantity FROM medicines WHERE id = ?", (prescription.medicine_id,))
        med_data = cursor.fetchone()
        if not med_data or med_data['quantity'] < prescription.quantity:
            raise ValueError("Not enough stock to fill prescription.")

        # Update inventory
        new_quantity = med_data['quantity'] - prescription.quantity
        cursor.execute("UPDATE medicines SET quantity = ? WHERE id = ?", (new_quantity, prescription.medicine_id))

        # Mark prescription as filled
        cursor.execute("UPDATE prescriptions SET filled = 1 WHERE id = ?", (prescription_id,))

        conn.commit()
        logging.info(f"Prescription with ID {prescription_id} filled successfully.")
        return True

    except (sqlite3.Error, ValueError) as e:
        conn.rollback()
        logging.error(f"Error filling prescription with ID {prescription_id}: {e}")
        return False
    finally:
        conn.close()
