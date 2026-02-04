"""Test suite for Example API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Example API with MongoDB"}


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "MongoDB" in data["message"]


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    """Test creating a new item."""
    item_data = {
        "name": "Test Item",
        "description": "Test Description",
        "price": 29.99
    }
    response = await client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "_id" in data


@pytest.mark.asyncio
async def test_create_item_without_description(client: AsyncClient):
    """Test creating an item without optional description."""
    item_data = {
        "name": "Simple Item",
        "price": 19.99
    }
    response = await client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] is None
    assert data["price"] == item_data["price"]


@pytest.mark.asyncio
async def test_list_items_empty(client: AsyncClient):
    """Test listing items when database is empty."""
    response = await client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient):
    """Test listing items."""
    # Create some items first
    items_data = [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "description": "Description 2", "price": 20.0}
    ]
    for item_data in items_data:
        await client.post("/items", json=item_data)
    
    response = await client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("_id" in item for item in data)


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient):
    """Test getting a specific item."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Get Test Item",
        "price": 15.50
    })
    item_id = create_response.json()["_id"]
    
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Get Test Item"
    assert data["price"] == 15.50


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient):
    """Test getting a non-existent item."""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
    response = await client.get(f"/items/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_item_invalid_id(client: AsyncClient):
    """Test getting an item with invalid ID format."""
    response = await client.get("/items/invalid-id")
    assert response.status_code == 400
    assert "Invalid item ID format" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    """Test deleting an item."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Delete Test Item",
        "price": 25.00
    })
    item_id = create_response.json()["_id"]
    
    response = await client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert item_id in response.json()["message"]
    
    # Verify item is deleted
    get_response = await client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_not_found(client: AsyncClient):
    """Test deleting a non-existent item."""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
    response = await client.delete(f"/items/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_invalid_id(client: AsyncClient):
    """Test deleting an item with invalid ID format."""
    response = await client.delete("/items/invalid-id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_patch_item_partial_update(client: AsyncClient):
    """Test partially updating an item."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Original Name",
        "description": "Original Description",
        "price": 30.00
    })
    item_id = create_response.json()["_id"]
    
    # Update only the price
    update_data = {"price": 35.00}
    response = await client.patch(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Original Name"
    assert data["description"] == "Original Description"
    assert data["price"] == 35.00


@pytest.mark.asyncio
async def test_patch_item_multiple_fields(client: AsyncClient):
    """Test updating multiple fields at once."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Old Name",
        "price": 40.00
    })
    item_id = create_response.json()["_id"]
    
    # Update name and description
    update_data = {
        "name": "New Name",
        "description": "New Description"
    }
    response = await client.patch(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New Description"
    assert data["price"] == 40.00  # Unchanged


@pytest.mark.asyncio
async def test_patch_item_empty_update(client: AsyncClient):
    """Test patching with no fields should return error."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Test Item",
        "price": 20.00
    })
    item_id = create_response.json()["_id"]
    
    # Try to update with empty data
    response = await client.patch(f"/items/{item_id}", json={})
    assert response.status_code == 400
    assert "No fields to update" in response.json()["detail"]


@pytest.mark.asyncio
async def test_patch_item_not_found(client: AsyncClient):
    """Test patching a non-existent item."""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
    response = await client.patch(f"/items/{fake_id}", json={"price": 50.00})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_item_invalid_id(client: AsyncClient):
    """Test patching an item with invalid ID format."""
    response = await client.patch("/items/invalid-id", json={"price": 50.00})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_patch_item_invalid_price(client: AsyncClient):
    """Test patching with invalid price (negative or zero)."""
    # Create an item first
    create_response = await client.post("/items", json={
        "name": "Test Item",
        "price": 20.00
    })
    item_id = create_response.json()["_id"]
    
    # Try to update with invalid price
    response = await client.patch(f"/items/{item_id}", json={"price": -5.00})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_patch_item_set_description_to_null(client: AsyncClient):
    """Test setting description to null explicitly."""
    # Create an item with description
    create_response = await client.post("/items", json={
        "name": "Test Item",
        "description": "Original Description",
        "price": 20.00
    })
    item_id = create_response.json()["_id"]
    
    # Set description to null
    response = await client.patch(f"/items/{item_id}", json={"description": None})
    assert response.status_code == 200
    data = response.json()
    assert data["description"] is None
    assert data["name"] == "Test Item"
    assert data["price"] == 20.00
