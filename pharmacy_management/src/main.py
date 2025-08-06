from fastapi import FastAPI
from typing import List
from . import schemas
from .services import inventory_service, patient_service, supplier_service, sales_service, prescription_service

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/medicines", response_model=List[schemas.Medicine])
def get_medicines():
    return inventory_service.get_all_medicines()

@app.get("/patients", response_model=List[schemas.Patient])
def get_patients():
    return patient_service.get_all_patients()

@app.get("/suppliers", response_model=List[schemas.Supplier])
def get_suppliers():
    return supplier_service.get_all_suppliers()

@app.get("/sales", response_model=List[schemas.Sale])
def get_sales():
    return sales_service.get_all_sales()

@app.get("/prescriptions/{patient_id}", response_model=List[schemas.Prescription])
def get_prescriptions_for_patient(patient_id: int):
    return prescription_service.get_prescriptions_by_patient(patient_id)
