from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class SaleItem:
    """Represents an item within a sale."""
    medicine_id: int
    quantity: int

@dataclass
class Sale:
    """Represents a sales transaction."""
    id: int
    timestamp: datetime
    user_id: int
    items: List[SaleItem] = field(default_factory=list)
