# CultHeld Frontend

React + Vite frontend for browsing cultural events.

## Setup

### Install dependencies

```bash
cd frontend
npm install
```

### Run locally

```bash
npm run dev
```

Frontend will open at `http://localhost:5173`

## Features

- **Event Table**: Browse all events with pagination
- **Filters**: Filter by venue, event type, and date range
- **Responsive Design**: Works on desktop and tablet
- **Event Type Badges**: Color-coded event type indicators
- **Direct Ticket Links**: Quick access to ticket purchase pages

## Components

- `App.jsx`: Main application component with state management
- `FilterBar.jsx`: Filter UI and controls
- `EventTable.jsx`: Event display table with formatting

## API Integration

Frontend calls the backend API at `http://localhost:8000/api`:
- `GET /events` - Fetch events with filters and pagination
- `GET /venues` - Fetch available venues
- `GET /event-types` - Fetch available event types

Make sure the backend is running before starting the frontend.
