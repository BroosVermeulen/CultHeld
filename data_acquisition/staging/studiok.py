import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import studiok as studiok_config
from utils.logging_config import get_logger
from utils.http_utils import safe_post, safe_json

logger = get_logger(__name__)


def studiok() -> pd.DataFrame:
    """Scrape Studio K events and return as DataFrame."""
    start_date = datetime.today()
    df = retrieve(start_date, studiok_config.DAYS_AHEAD)
    if len(df) == 0:
        logger.warning("No Studio K events found")
        return df
    df = post_process(df)
    logger.info(f"Scraped {len(df)} Studio K events")
    return df


def retrieve(start_date: datetime, days: int) -> pd.DataFrame:
    """Fetch events for the next N days."""
    events = []
    for i in range(0, days):
        check_date = start_date + timedelta(days=i)
        day_events = api_call(check_date)
        events.extend(day_events)
    
    df = pd.DataFrame(events)
    return df


def post_process(df: pd.DataFrame) -> pd.DataFrame:
    """Transform Studio K data to common schema."""
    if df.empty:
        return df
    
    # Convert start_date_time to datetime
    # parse as UTC then convert to Amsterdam timezone
    df['start_date_time'] = pd.to_datetime(df['start_date_time'], errors='coerce', utc=True).dt.tz_convert('Europe/Amsterdam')
    
    df['venue'] = 'Studio K'
    df['price'] = 12
    
    # include title for mapping
    return df[['venue', 'start_date_time', 'ticket_url', 'price', 'title']]


def api_call(check_date: datetime) -> list:
    """Call Studio K API for a specific date."""
    date_str = check_date.strftime('%Y-%m-%d')
    
    url = studiok_config.BASE_URL + studiok_config.API_ENDPOINT
    payload = f"action=loadShows&date={date_str}"
    
    try:
        response = safe_post(url, data=payload, headers=studiok_config.HEADERS, timeout=10)
        response.raise_for_status()
        
        try:
            json_data = safe_json(response)
        except Exception:
            # fallback: try to decode text
            text = response.text
            # if it looks like JSON, try json.loads
            try:
                import json as _json
                json_data = _json.loads(text)
            except Exception:
                logger.warning("Studio K returned non-JSON response for %s", date_str)
                return []
        soup = BeautifulSoup(json_data.get('html', ''), 'html.parser')
        
        events = []
        # Parse both main list and slideout list
        for li in soup.find_all('li'):
            time_elem = li.find('a', class_='time')
            title_elem = li.find('a', class_='title')
            
            if time_elem and title_elem:
                time_str = time_elem.text.strip()
                title = title_elem.text.strip()
                ticket_url = title_elem.get('href', '')
                
                event = {
                    'start_date_time': f"{date_str} {time_str}",
                    'title': title,
                    'ticket_url': ticket_url,
                }
                events.append(event)
        
        return events
    except Exception as e:
        logger.warning(f"Failed to scrape Studio K ({date_str}): {e}")
        return []
