from dataclasses import dataclass

@dataclass
class User:
    """Represents a user of the system."""
    id: int
    username: str
    password_hash: str
    role_id: int
