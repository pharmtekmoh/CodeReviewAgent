from dataclasses import dataclass

@dataclass
class Patient:
    """Represents a patient in the pharmacy."""
    id: int
    name: str
    address: str
    phone: str
