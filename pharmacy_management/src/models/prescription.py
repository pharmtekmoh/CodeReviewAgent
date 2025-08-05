from dataclasses import dataclass
from datetime import date

@dataclass
class Prescription:
    """Represents a prescription."""
    id: int
    patient_id: int
    doctor_name: str
    medicine_id: int
    quantity: int
    prescription_date: date
    filled: bool
