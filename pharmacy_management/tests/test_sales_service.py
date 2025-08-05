import pytest
from datetime import datetime
from src.services import sales_service
from src.models.sale import Sale, SaleItem

def test_create_sale(monkeypatch):
    """Tests creating a new sale."""

    class MockCursor:
        def __init__(self):
            self.lastrowid = 1

        def execute(self, query, *args):
            if "SELECT price, quantity FROM medicines" in query:
                self._fetchone_result = {'price': 10.0, 'quantity': 100}
            else:
                self._fetchone_result = None

        def fetchone(self):
            return self._fetchone_result

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def execute(self, *args, **kwargs):
            pass

        def commit(self):
            pass

        def rollback(self):
            pass

        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('src.services.sales_service.get_db_connection', mock_get_db_connection)

    items = [SaleItem(medicine_id=1, quantity=2)]
    sale = sales_service.create_sale(1, items)

    assert sale is not None
    assert sale.id == 1
    assert len(sale.items) == 1
