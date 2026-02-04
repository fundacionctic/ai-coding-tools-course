"""Pytest configuration and fixtures."""
import os
import sys
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set test database environment variables
os.environ["MONGODB_URL"] = os.getenv("TEST_MONGODB_URL", "mongodb://admin:password@localhost:27017")
os.environ["MONGODB_DB_NAME"] = "test_example_api"

from example_api.main import app, database, mongodb_client


@pytest.fixture(scope="function")
async def client():
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def clean_database():
    """Clean the database before and after each test."""
    # Setup: ensure app is started and clean database
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ):
        if database is not None:
            # Clean all collections
            await database["items"].delete_many({})
        
        yield
        
        # Teardown: clean database after test
        if database is not None:
            await database["items"].delete_many({})
