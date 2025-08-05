from dataclasses import dataclass

@dataclass
class Supplier:
    """Represents a supplier of medicines."""
    id: int
    name: str
    contact_person: str
    phone: str
    address: str
