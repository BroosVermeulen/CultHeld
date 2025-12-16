# CultHeld Data Acquisition

Automated data scraper and transformation pipeline for Amsterdam cultural venues (Melkweg, Paradiso).

## Overview

This module:
- **Scrapes** current events from Melkweg and Paradiso APIs
- **Maps** raw data to a standardized core schema
- **Stores** events in DuckDB for analysis

## Quick Start

```bash
cd data_acquisition
poetry install
poetry run python run_all.py
```

## Architecture

### Staging (`staging/`)
Raw scrapers that fetch event data from venue APIs.
- `melkweg.py` - Scrapes Melkweg agenda (Next.js powered)
- `paradiso.py` - Queries Paradiso GraphQL API

**Output**: Raw DataFrames with venue-specific fields

### Mapping (`mapping/`)
Transforms venue-specific data to standardized schema.
- `melkweg_mapping.py` - Maps Melkweg fields
- `paradiso_mapping.py` - Maps Paradiso fields

**Schema**: `venue`, `title`, `start_date_time`, `price`, `ticket_url`

### Core (`core/`)
Database operations and transformations.
- `transform.py` - Writes events to DuckDB

**Database**: `data/core/events.duckdb`

### Utils
Helper functions for common operations.
- `duckdb_utils.py` - Database helpers
- `staging_utils.py` - File I/O (CSV export)

## Data Flow

```
Staging (melkweg.py, paradiso.py)
    ↓ (raw DataFrame)
Mapping (melkweg_mapping.py, paradiso_mapping.py)
    ↓ (mapped dict per row)
Core (transform.py → write_core_records)
    ↓
DuckDB (data/core/events.duckdb)
```

## Data Directories

- `data/core/` - DuckDB database with processed events
- `data/staging/` - Temporary CSV exports of raw scraped data

## Scrapers Details

### Melkweg
- **Endpoint**: Next.js data API (`/_next/data/{buildId}/nl/agenda.json`)
- **Auth**: None (public endpoint)
- **Features**: Auto-fetches build ID to avoid stale tokens
- **Fields**: `url`, `startDate`, `name`, etc.

### Paradiso
- **Endpoint**: GraphQL API (`gqlcache-production.paradiso.workers.dev/graphql`)
- **Auth**: Bearer token (in headers)
- **Fields**: `uri`, `startDateTime`, `title`, `price`, etc.

## Setup & Configuration

### Dependencies
See `pyproject.toml`:
- `pandas` - Data manipulation
- `requests` - HTTP requests
- `duckdb` - Local database
- `beautifulsoup4` - HTML parsing (if needed)

### Environment
- Python: 3.12
- Poetry: for dependency management

## Running the Pipeline

Execute all scrapers with unified mapping:
```bash
poetry run python run_all.py
```

Logs show:
- Scraper name and row count
- Mapping completion message
- Sample of mapped data (head)
- Database write confirmation

## Troubleshooting

**Melkweg API fails**: Build ID may have changed. The auto-fetch should handle this, but check the URL manually at https://www.melkweg.nl/nl/agenda.

**Paradiso API fails**: Check the Bearer token in `paradiso.py` headers—may have expired.

**Database write fails**: Ensure `data/core/` directory exists and is writable.

## Future Improvements

- [ ] Move secrets (tokens, cookies) to `.env`
- [ ] Add caching layer to avoid redundant API calls
- [ ] Implement incremental updates instead of full re-scrapes
- [ ] Add error handling and retry logic
- [ ] Create REST API for event queries
