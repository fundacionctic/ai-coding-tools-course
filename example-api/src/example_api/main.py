import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId


# MongoDB connection
mongodb_client: AsyncIOMotorClient = None
database = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MongoDB connection lifecycle."""
    global mongodb_client, database
    
    # Startup
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "example_api")
    
    mongodb_client = AsyncIOMotorClient(mongodb_url)
    database = mongodb_client[db_name]
    
    # Verify connection
    try:
        await mongodb_client.admin.command('ping')
        print(f"Connected to MongoDB at {mongodb_url}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    
    yield
    
    # Shutdown
    mongodb_client.close()


app = FastAPI(
    title="Example API",
    description="A simple FastAPI example application with MongoDB",
    version="0.1.0",
    lifespan=lifespan
)


class HealthResponse(BaseModel):
    status: str
    message: str


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)


class Item(ItemCreate):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


def get_items_collection():
    """Get the items collection from the database."""
    return database["items"]


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with welcome message."""
    return {"message": "Welcome to Example API with MongoDB"}


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health():
    """Health check endpoint."""
    try:
        await mongodb_client.admin.command('ping')
        return HealthResponse(status="healthy", message="API and MongoDB are running")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MongoDB unavailable: {str(e)}")


@app.get("/items", tags=["Items"])
async def list_items():
    """List all items."""
    collection = get_items_collection()
    items = []
    async for item in collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items


@app.post("/items", status_code=201, tags=["Items"])
async def create_item(item: ItemCreate):
    """Create a new item."""
    collection = get_items_collection()
    item_dict = item.model_dump()
    result = await collection.insert_one(item_dict)
    
    created_item = await collection.find_one({"_id": result.inserted_id})
    created_item["_id"] = str(created_item["_id"])
    return created_item


@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: str):
    """Get a specific item by ID."""
    collection = get_items_collection()
    
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    
    item = await collection.find_one({"_id": object_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item["_id"] = str(item["_id"])
    return item


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: str):
    """Delete a specific item by ID."""
    collection = get_items_collection()
    
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    
    result = await collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": f"Item {item_id} deleted"}


@app.patch("/items/{item_id}", tags=["Items"])
async def update_item(item_id: str, item: ItemUpdate):
    """Partially update a specific item by ID."""
    collection = get_items_collection()
    
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    
    # Get only the fields that were explicitly set in the request
    update_data = item.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update the item in MongoDB
    result = await collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Fetch and return the updated item
    updated_item = await collection.find_one({"_id": object_id})
    updated_item["_id"] = str(updated_item["_id"])
    return updated_item
