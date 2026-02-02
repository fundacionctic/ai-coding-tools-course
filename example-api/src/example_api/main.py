from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Example API",
    description="A simple FastAPI example application",
    version="0.1.0"
)


class HealthResponse(BaseModel):
    status: str
    message: str


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class Item(ItemCreate):
    id: int


# In-memory storage
items_db: dict[int, Item] = {}
next_id = 1


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with welcome message."""
    return {"message": "Welcome to Example API"}


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health():
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="API is running")


@app.get("/items", response_model=list[Item], tags=["Items"])
async def list_items():
    """List all items."""
    return list(items_db.values())


@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
async def create_item(item: ItemCreate):
    """Create a new item."""
    global next_id
    new_item = Item(id=next_id, **item.model_dump())
    items_db[next_id] = new_item
    next_id += 1
    return new_item


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in items_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete a specific item by ID."""
    if item_id not in items_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted"}
