# Example API

A simple FastAPI example application demonstrating basic CRUD operations.

## Features

- FastAPI web framework
- Pydantic models for request/response validation
- In-memory data storage
- RESTful API endpoints
- Interactive API documentation (Swagger UI)

## Setup

This project uses [uv](https://github.com/astral-sh/uv) as the build system and package manager.

### Installation

```bash
# Install dependencies
uv sync

# Or if you need to create the virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Running the API

### Development Mode (with auto-reload)

```bash
uv run uvicorn example_api.main:app --reload --host 127.0.0.1 --port 8000
```

### Production Mode

```bash
uv run uvicorn example_api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### General

- `GET /` - Welcome message
- `GET /health` - Health check

### Items

- `GET /items` - List all items
- `POST /items` - Create a new item
- `GET /items/{item_id}` - Get a specific item
- `DELETE /items/{item_id}` - Delete a specific item

## Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Create an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Example Item", "description": "A test item", "price": 9.99}'

# List all items
curl http://localhost:8000/items

# Get specific item
curl http://localhost:8000/items/1

# Delete an item
curl -X DELETE http://localhost:8000/items/1
```

## Project Structure

```
example-api/
├── src/
│   └── example_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI application
│       └── py.typed
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── README.md
```

## Development

### Adding Dependencies

```bash
uv add <package-name>
```

### Running with Different Settings

```bash
# Custom host and port
uv run uvicorn example_api.main:app --host 127.0.0.1 --port 3000

# With auto-reload
uv run uvicorn example_api.main:app --reload
```
