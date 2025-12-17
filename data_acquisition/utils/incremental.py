"""Incremental update tracking for scrapers."""

import json
from datetime import datetime
from pathlib import Path

from utils.logging_config import get_logger

logger = get_logger(__name__)

STATE_FILE = Path("data/scraper_state.json")


def get_last_run(venue: str) -> str | None:
    """
    Get the last successful scrape timestamp for a venue.
    
    Args:
        venue: Venue name (e.g., 'Melkweg', 'Paradiso')
        
    Returns:
        ISO format datetime string or None if never run
    """
    if not STATE_FILE.exists():
        return None
    
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        return state.get(venue, {}).get("last_run")
    except Exception as e:
        logger.warning(f"Failed to read scraper state: {e}")
        return None


def set_last_run(venue: str, timestamp: str | None = None) -> None:
    """
    Update the last successful scrape timestamp for a venue.
    
    Args:
        venue: Venue name
        timestamp: ISO format datetime (defaults to now)
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    state = {}
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read existing state: {e}")
    
    # Ensure data directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Update state
    if venue not in state:
        state[venue] = {}
    state[venue]["last_run"] = timestamp
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info(f"Updated last run for {venue}: {timestamp}")
    except Exception as e:
        logger.error(f"Failed to write scraper state: {e}")


def should_update(venue: str, min_hours: int = 24) -> bool:
    """
    Check if a venue should be updated based on time since last run.
    
    Args:
        venue: Venue name
        min_hours: Minimum hours between updates (default 24)
        
    Returns:
        True if venue should be updated, False otherwise
    """
    last_run = get_last_run(venue)
    if last_run is None:
        logger.info(f"No previous run for {venue}, will update")
        return True
    
    try:
        last_run_dt = datetime.fromisoformat(last_run)
        now = datetime.now()
        hours_elapsed = (now - last_run_dt).total_seconds() / 3600
        
        should_run = hours_elapsed >= min_hours
        if should_run:
            logger.info(f"{venue}: {hours_elapsed:.1f}h since last run, will update")
        else:
            logger.info(f"{venue}: only {hours_elapsed:.1f}h since last run, skipping")
        
        return should_run
    except Exception as e:
        logger.warning(f"Failed to parse last run time: {e}, will update")
        return True
