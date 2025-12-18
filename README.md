# CultHeld - Full Stack Application

Local development setup for the CultHeld events platform.

## Project Structure

```
CultHeld/
├── data_acquisition/     # Data scraping and pipeline
│   ├── staging/
│   ├── mapping/
│   ├── core/
│   ├── utils/
│   ├── config/
│   ├── data/core/events.duckdb  # Main database
│   └── pyproject.toml
├── backend/              # FastAPI REST API
│   ├── app.py
│   ├── pyproject.toml
│   └── README.md
├── frontend/             # React + Vite UI
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
└── README.md
```

## Quick Start (Local Development)

### Terminal 1: Backend

```bash
cd backend
poetry install --no-root
poetry run uvicorn app:app --reload
```

Backend runs on: **http://localhost:8000**
- API docs: http://localhost:8000/docs

### Terminal 2: Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:5173**

### Terminal 3: Data Pipeline (Optional)

```bash
cd data_acquisition
poetry run python run_all.py
```

## API Endpoints

### Events
- `GET /api/events?venue=Melkweg&event_type=Concert&page=1&limit=50`
- `GET /api/venues`
- `GET /api/event-types`
- `GET /health`

## Features

✅ Event scraping (7 venues)  
✅ Data validation & deduplication  
✅ FastAPI REST backend  
✅ React table with filtering  
✅ Pagination  
✅ Latest event logic (window functions)  
✅ Color-coded event types  

## Tech Stack

- **Backend**: Python, FastAPI, DuckDB, Poetry
- **Frontend**: React, Vite, Axios, CSS
- **Database**: DuckDB (embedded, no setup needed)

## Next Steps

1. Run backend and frontend locally
2. Browse events at http://localhost:5173
3. Test filters and pagination
4. Plan deployment when ready
