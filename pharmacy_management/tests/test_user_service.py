import pytest
from src.services import user_service
from src.models.user import User

def test_create_user(monkeypatch):
    """Tests the creation of a new user."""

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

    monkeypatch.setattr('src.services.user_service.get_db_connection', mock_get_db_connection)

    user = user_service.create_user("testuser", "password", "pharmacist")

    assert user is not None
    assert user.id == 1
    assert user.username == "testuser"
    assert user.role == "pharmacist"

def test_get_user_by_username(monkeypatch):
    """Tests retrieving a user by username."""

    class MockCursor:
        def execute(self, *args, **kwargs):
            pass

        def fetchone(self):
            return {'id': 1, 'username': 'testuser', 'password_hash': 'hashed_password', 'role': 'pharmacist'}

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('src.services.user_service.get_db_connection', mock_get_db_connection)

    user = user_service.get_user_by_username("testuser")

    assert user is not None
    assert user.id == 1
    assert user.username == "testuser"

def test_check_user(monkeypatch):
    """Tests checking a user's credentials."""

    # The correct hash for 'password' is '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
    def mock_get_user_by_username(username):
        return User(id=1, username=username, password_hash='5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', role='pharmacist')

    monkeypatch.setattr('src.services.user_service.get_user_by_username', mock_get_user_by_username)

    user = user_service.check_user("testuser", "password")

    assert user is not None
    assert user.username == "testuser"
