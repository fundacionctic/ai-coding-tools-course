"""Pytest configuration and fixtures."""
import os
import sys
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set test database environment variables before importing the app
os.environ["MONGODB_URL"] = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")
os.environ["MONGODB_DB_NAME"] = "test_example_api"

from example_api.main import app


@pytest.fixture(scope="function")
async def client():
    """Create an async test client that properly triggers the lifespan context."""
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url="http://test"
        ) as ac:
            yield ac


@pytest.fixture(scope="function", autouse=True)
async def clean_database():
    """Clean the database before and after each test."""
    # Create a direct connection to the test database for cleanup
    mongodb_url = os.environ["MONGODB_URL"]
    db_name = os.environ["MONGODB_DB_NAME"]
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[db_name]
    
    # Setup: clean database before test
    await db["items"].delete_many({})
    
    yield
    
    # Teardown: clean database after test
    await db["items"].delete_many({})
    
    # Close the connection
    client.close()
