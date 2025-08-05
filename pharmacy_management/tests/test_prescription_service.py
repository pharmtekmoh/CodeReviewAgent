import pytest
from datetime import date
from src.services import prescription_service
from src.models.prescription import Prescription

def test_create_prescription(monkeypatch):
    """Tests creating a new prescription."""

    class MockCursor:
        def execute(self, *args, **kwargs):
            pass

        @property
        def lastrowid(self):
            return 1

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def commit(self):
            pass

        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('src.services.prescription_service.get_db_connection', mock_get_db_connection)

    pres_date = date(2023, 1, 1)
    prescription = prescription_service.create_prescription(1, "Dr. Test", 1, 30, pres_date)

    assert prescription is not None
    assert prescription.id == 1
    assert prescription.doctor_name == "Dr. Test"
