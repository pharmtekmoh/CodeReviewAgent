from pydantic import BaseModel
from datetime import date, datetime
from typing import List

class Medicine(BaseModel):
    id: int
    name: str
    manufacturer: str
    price: float
    quantity: int
    expiry_date: date

    class Config:
        orm_mode = True

class Patient(BaseModel):
    id: int
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    id: int
    name: str
    contact_person: str
    phone: str
    address: str

    class Config:
        orm_mode = True

class SaleItem(BaseModel):
    medicine_id: int
    quantity: int

class Sale(BaseModel):
    id: int
    timestamp: datetime
    user_id: int
    items: List[SaleItem]

    class Config:
        orm_mode = True

class Prescription(BaseModel):
    id: int
    patient_id: int
    doctor_name: str
    medicine_id: int
    quantity: int
    prescription_date: date
    filled: bool

    class Config:
        orm_mode = True
