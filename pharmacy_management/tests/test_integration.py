import pytest
from src.services import user_service
from src.utils import database

def test_user_integration(test_db, monkeypatch):
    """Integration test for the user service."""

    # Override the get_db_connection to use the test database
    def mock_get_db_connection():
        return database.get_db_connection(db_path=test_db)

    monkeypatch.setattr('src.services.user_service.get_db_connection', mock_get_db_connection)

    # 1. Create a user
    created_user = user_service.create_user("integ_test", "password", "admin")
    assert created_user is not None
    assert created_user.username == "integ_test"

    # 2. Retrieve the user and verify
    retrieved_user = user_service.get_user_by_username("integ_test")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "integ_test"
