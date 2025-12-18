# Railway Deployment Guide

## Setup Railway

1. Go to https://railway.app
2. Sign up with GitHub (free)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Connect your GitHub account and select the CultHeld repository
6. Choose the `backend` folder as the root directory

## Environment Variables

Railway will auto-detect Python and install dependencies. You'll need to:

1. Upload the DuckDB file:
   - Copy `data_acquisition/data/core/events.duckdb` to `backend/events.duckdb`
   - Commit and push

2. Update `app.py` to use the local file in production

## Domain

Railway provides a free domain like: `your-app.up.railway.app`

Copy this URL - you'll need it for the frontend!
