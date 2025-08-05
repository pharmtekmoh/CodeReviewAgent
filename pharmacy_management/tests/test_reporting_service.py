import pytest
from src.services import reporting_service

def test_get_inventory_value(monkeypatch):
    """Tests calculating the inventory value."""

    class MockCursor:
        def execute(self, *args, **kwargs):
            pass

        def fetchone(self):
            return {'total_value': 1234.56}

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('src.services.reporting_service.get_db_connection', mock_get_db_connection)

    value = reporting_service.get_inventory_value()

    assert value == 1234.56
