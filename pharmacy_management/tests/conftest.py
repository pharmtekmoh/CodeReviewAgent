import pytest
import os
from src.utils import database

@pytest.fixture(scope="session")
def test_db():
    """Fixture to set up and tear down a temporary database for testing."""
    db_path = "data/test_pharmacy.db"

    # Ensure any old test DB is removed
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create tables in the new test DB
    database.create_tables(db_path)

    yield db_path

    # Teardown: clean up the test database
    if os.path.exists(db_path):
        os.remove(db_path)
