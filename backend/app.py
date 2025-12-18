"""FastAPI backend for CultHeld events API."""

import os
from datetime import datetime
from pathlib import Path

import duckdb
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configuration
# In production, use local events.duckdb; in dev, use data_acquisition path
# Check if running on Railway/Render by looking for environment indicators
is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER") or os.getenv("RAILWAY_TOKEN") or os.path.exists("/app")

if is_production:
    DB_PATH = Path("/app/backend/events.duckdb")
    # Fallback if the above doesn't exist
    if not DB_PATH.exists():
        DB_PATH = Path(__file__).parent / "events.duckdb"
else:
    DB_PATH = Path(__file__).parent.parent / "data_acquisition" / "data" / "core" / "events.duckdb"

# CORS: Allow your domain in production
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*.siteground.com",  # Adjust to your actual domain
    os.getenv("FRONTEND_URL", ""),  # Set this in Railway
]

app = FastAPI(
    title="CultHeld Events API",
    description="API for querying cultural events from DuckDB",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class Event(BaseModel):
    venue: str
    event_type: str
    event_name: str
    start_date_time: str
    ticket_url: str
    price: float | None


class EventsResponse(BaseModel):
    total: int
    page: int
    limit: int
    events: list[Event]


def get_db_connection():
    """Get a read-only DuckDB connection."""
    return duckdb.connect(database=str(DB_PATH), read_only=True)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    print(f"Starting CultHeld API")
    print(f"DB_PATH: {DB_PATH}")
    print(f"DB exists: {DB_PATH.exists()}")
    try:
        conn = get_db_connection()
        result = conn.execute("SELECT COUNT(*) as count FROM events").fetchall()
        print(f"Database connected. Total events: {result[0][0]}")
        conn.close()
    except Exception as e:
        print(f"Database error on startup: {e}")


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/events", response_model=EventsResponse)
async def get_events(
    venue: str | None = Query(None, description="Filter by venue"),
    event_type: str | None = Query(None, description="Filter by event type"),
    start_date: str | None = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(50, ge=1, le=500, description="Results per page"),
) -> EventsResponse:
    """Get events with optional filters and pagination."""
    try:
        con = get_db_connection()

        # Build base query with latest events (using window function)
        query = """
        SELECT 
            venue, event_type, event_name, start_date_time, ticket_url, price
        FROM (
            SELECT 
                venue, event_type, event_name, start_date_time, ticket_url, price, as_of_date,
                ROW_NUMBER() OVER (
                    PARTITION BY venue, event_name, start_date_time 
                    ORDER BY as_of_date DESC
                ) as rn
            FROM events
        )
        WHERE rn = 1
        """

        filters = []
        params = {}

        # Add filters
        if venue:
            filters.append("venue = ?")
            params["venue"] = venue

        if event_type:
            filters.append("event_type = ?")
            params["event_type"] = event_type

        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                filters.append("DATE(start_date_time) >= ?")
                params["start_date"] = start_date
            except ValueError:
                pass

        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
                filters.append("DATE(start_date_time) <= ?")
                params["end_date"] = end_date
            except ValueError:
                pass

        # Append additional filters if they exist
        if filters:
            query += " AND " + " AND ".join(filters)

        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM ({query})"
        total = con.execute(
            count_query,
            [params.get(k) for k in ["venue", "event_type", "start_date", "end_date"]
             if k in params and params[k] is not None],
        ).fetchone()[0]

        # Add pagination
        offset = (page - 1) * limit
        query += f" ORDER BY start_date_time ASC LIMIT ? OFFSET ?"

        # Execute query with parameters
        param_values = [params.get(k) for k in ["venue", "event_type", "start_date", "end_date"]
                        if k in params and params[k] is not None]
        param_values.extend([limit, offset])

        result = con.execute(query, param_values).fetchall()
        con.close()

        # Map results to Event objects
        events = [
            Event(
                venue=row[0],
                event_type=row[1],
                event_name=row[2],
                start_date_time=str(row[3]),
                ticket_url=row[4],
                price=row[5],
            )
            for row in result
        ]

        return EventsResponse(
            total=total,
            page=page,
            limit=limit,
            events=events,
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return EventsResponse(
            total=0,
            page=page,
            limit=limit,
            events=[],
        )


@app.get("/api/venues")
async def get_venues() -> dict:
    """Get list of unique venues."""
    try:
        con = get_db_connection()
        venues = con.execute(
            "SELECT DISTINCT venue FROM events ORDER BY venue"
        ).fetchall()
        con.close()
        return {"venues": [v[0] for v in venues]}
    except Exception as e:
        return {"venues": []}


@app.get("/api/event-types")
async def get_event_types() -> dict:
    """Get list of unique event types."""
    try:
        con = get_db_connection()
        types = con.execute(
            "SELECT DISTINCT event_type FROM events ORDER BY event_type"
        ).fetchall()
        con.close()
        return {"event_types": [t[0] for t in types]}
    except Exception as e:
        return {"event_types": []}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
