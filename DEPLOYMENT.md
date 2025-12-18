# Deployment Checklist

## Backend (Railway)

### 1. Push to GitHub
```bash
cd /Users/broosvermeulen/Documents/code/CultHeld
git add backend/
git commit -m "Add backend deployment config"
git push origin main
```

### 2. Copy DuckDB file to backend
```bash
cp data_acquisition/data/core/events.duckdb backend/events.duckdb
git add backend/events.duckdb
git commit -m "Add production database"
git push
```

### 3. Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your repo → Choose `backend` folder
5. Railway auto-detects Python and deploys
6. Copy your Railway URL (e.g., `https://cultheld-backend.up.railway.app`)

### 4. Set Environment Variable
In Railway dashboard:
- Go to Variables tab
- Add: `FRONTEND_URL` = `https://yourdomain.com` (your Siteground domain)

---

## Frontend (Siteground)

### 1. Build for production
Update API URL in frontend first:

Edit `frontend/src/App.jsx`:
```javascript
const API_BASE = 'https://your-railway-url.up.railway.app/api'
```

Then build:
```bash
cd frontend
npm run build
```

This creates a `dist/` folder with static files.

### 2. Upload to Siteground
1. Log into Siteground cPanel
2. Go to File Manager
3. Navigate to `public_html/` (or your domain folder)
4. Upload all files from `frontend/dist/`
5. Access your site at your domain!

---

## Update Workflow (when you add new events)

1. Run scraper locally: `cd data_acquisition && poetry run python run_all.py`
2. Copy new DB: `cp data_acquisition/data/core/events.duckdb backend/events.duckdb`
3. Commit and push: `git add backend/events.duckdb && git commit -m "Update events" && git push`
4. Railway auto-deploys the new DB!
