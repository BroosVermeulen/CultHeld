# CultHeld Backend

FastAPI-based REST API for querying cultural events from DuckDB.

## Setup

### Install dependencies

```bash
cd backend
poetry install
```

### Run locally

```bash
poetry run uvicorn app:app --reload
```

API will be available at `http://localhost:8000`
- Swagger UI docs: `http://localhost:8000/docs`
- ReDoc docs: `http://localhost:8000/redoc`

## API Endpoints

### `GET /health`
Health check endpoint.

### `GET /api/events`
Retrieve events with optional filtering and pagination.

**Query Parameters:**
- `venue` (optional): Filter by venue name
- `event_type` (optional): Filter by event type (Actualiteit, Bioscoop, Concert, Theater, Museum)
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 50, max: 500)

**Example:**
```
GET /api/events?venue=Melkweg&event_type=Concert&page=1&limit=20
```

**Response:**
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "events": [
    {
      "venue": "Melkweg",
      "event_type": "Concert",
      "event_name": "Example Concert",
      "start_date_time": "2025-12-25T20:00:00+01:00",
      "ticket_url": "https://example.com",
      "price": 25.0
    }
  ]
}
```

### `GET /api/venues`
Get list of all unique venues.

**Response:**
```json
{
  "venues": ["Melkweg", "Paradiso", "De Balie", ...]
}
```

### `GET /api/event-types`
Get list of all unique event types.

**Response:**
```json
{
  "event_types": ["Actualiteit", "Bioscoop", "Concert", "Theater", "Museum"]
}
```

## Database

The API reads from `../data_acquisition/data/core/events.duckdb` in read-only mode.
Always queries the latest version of each event using window functions.
