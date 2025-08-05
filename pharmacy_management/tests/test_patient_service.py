import pytest
from src.services import patient_service
from src.models.patient import Patient

def test_add_patient(monkeypatch):
    """Tests adding a new patient."""

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

    monkeypatch.setattr('src.services.patient_service.get_db_connection', mock_get_db_connection)

    patient = patient_service.add_patient("Test Patient", "123 Test St", "555-1234")

    assert patient is not None
    assert patient.id == 1
    assert patient.name == "Test Patient"
