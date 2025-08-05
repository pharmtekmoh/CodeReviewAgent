import pytest
from src.services import supplier_service
from src.models.supplier import Supplier

def test_add_supplier(monkeypatch):
    """Tests adding a new supplier."""

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

    monkeypatch.setattr('src.services.supplier_service.get_db_connection', mock_get_db_connection)

    supplier = supplier_service.add_supplier("Test Supplier", "Mr. Test", "555-5678", "456 Test Ave")

    assert supplier is not None
    assert supplier.id == 1
    assert supplier.name == "Test Supplier"
