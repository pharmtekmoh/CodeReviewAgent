from dataclasses import dataclass
from datetime import date

@dataclass
class Medicine:
    """Represents a medicine in the pharmacy."""
    id: int
    name: str
    manufacturer: str
    price: float
    quantity: int
    expiry_date: date
