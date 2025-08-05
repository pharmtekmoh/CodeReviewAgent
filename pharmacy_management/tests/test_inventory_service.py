import pytest
from datetime import date
from src.services import inventory_service
from src.models.medicine import Medicine

def test_add_medicine(monkeypatch):
    """Tests adding a new medicine."""

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

    monkeypatch.setattr('src.services.inventory_service.get_db_connection', mock_get_db_connection)

    expiry = date(2025, 12, 31)
    medicine = inventory_service.add_medicine("Test Med", "Test Corp", 10.0, 100, expiry, 1)

    assert medicine is not None
    assert medicine.id == 1
    assert medicine.name == "Test Med"

def test_get_medicine_by_id(monkeypatch):
    """Tests retrieving a medicine by its ID."""

    class MockCursor:
        def execute(self, *args, **kwargs):
            pass

        def fetchone(self):
            return {'id': 1, 'name': 'Test Med', 'manufacturer': 'Test Corp', 'price': 10.0, 'quantity': 100, 'expiry_date': '2025-12-31', 'supplier_id': 1}

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('src.services.inventory_service.get_db_connection', mock_get_db_connection)

    medicine = inventory_service.get_medicine_by_id(1)

    assert medicine is not None
    assert medicine.id == 1
    assert medicine.name == "Test Med"
