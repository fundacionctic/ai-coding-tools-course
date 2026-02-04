# Example API

A simple FastAPI example application demonstrating basic CRUD operations with MongoDB.

## Features

- FastAPI web framework
- MongoDB database with Motor (async driver)
- Pydantic models for request/response validation
- RESTful API endpoints
- Interactive API documentation (Swagger UI)
- Docker Compose for local development

## Setup

This project uses [uv](https://github.com/astral-sh/uv) as the build system and package manager.

### Local Development (without Docker)

#### Prerequisites
- Python 3.11+
- MongoDB running locally or accessible remotely

#### Installation

```bash
# Install dependencies
uv sync

# Set environment variables (optional)
export MONGODB_URL="mongodb://admin:password@localhost:27017"
export MONGODB_DB_NAME="example_api"
```

#### Running the API

```bash
# Development mode with auto-reload
uv run uvicorn example_api.main:app --reload --host 127.0.0.1 --port 8000
```

### Docker Compose (Recommended)

The easiest way to run the full stack (API + MongoDB):

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes (clears database)
docker compose down -v
```

The API will be available at `http://localhost:8000`
MongoDB will be available at `localhost:27017`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### General

- `GET /` - Welcome message
- `GET /health` - Health check (includes MongoDB connectivity)

### Items

- `GET /items` - List all items
- `POST /items` - Create a new item
- `GET /items/{item_id}` - Get a specific item by MongoDB ObjectId
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

# Get specific item (use ID from previous response)
curl http://localhost:8000/items/6582a1b2c3d4e5f6a7b8c9d0

# Delete an item
curl -X DELETE http://localhost:8000/items/6582a1b2c3d4e5f6a7b8c9d0
```

## Environment Variables

| Variable         | Description                    | Default                                    |
| ---------------- | ------------------------------ | ------------------------------------------ |
| `MONGODB_URL`    | MongoDB connection string      | `mongodb://admin:password@localhost:27017` |
| `MONGODB_DB_NAME`| MongoDB database name          | `example_api`                              |

## Project Structure

```
example-api/
├── src/
│   └── example_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI application with MongoDB
│       └── py.typed
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image for the API
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
├── .gitignore
└── README.md
```

## Docker Services

### API Service
- Built from local Dockerfile
- Exposes port 8000
- Connects to MongoDB service
- Auto-restarts on failure

### MongoDB Service
- Uses official MongoDB 8.0 image
- Exposes port 27017
- Persistent volume for data storage
- Health checks enabled
- Credentials: admin/password (change in production!)

## Development

### Running Tests

Tests require MongoDB to be running. Start MongoDB with docker-compose:

```bash
# Start MongoDB
docker compose up -d mongodb

# Run all tests
uv run pytest tests/

# Run tests with verbose output
uv run pytest tests/ -v

# Run a specific test
uv run pytest tests/test_api.py::test_create_item -v
```

### Adding Dependencies

```bash
uv add <package-name>
```

### Accessing MongoDB

Connect to the MongoDB instance:

```bash
# Using mongosh (if installed locally)
mongosh mongodb://localhost:27017

# Using Docker
docker compose exec mongodb mongosh
```

### Rebuilding Docker Images

```bash
# Rebuild after code changes
docker compose build

# Rebuild and restart
docker compose up -d --build
```

## Production Considerations

⚠️ **Important**: This is a development example. For production:

1. Change MongoDB credentials
2. Use environment variables or secrets management
3. Add authentication to the API
4. Enable TLS/SSL for MongoDB
5. Add proper error logging
6. Implement rate limiting
7. Add data validation and sanitization
8. Use connection pooling appropriately
