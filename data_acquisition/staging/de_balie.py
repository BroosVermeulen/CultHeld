import requests
import json
import pandas as pd
from io import StringIO
from config import de_balie as de_balie_config
from utils.logging_config import get_logger

logger = get_logger(__name__)


def scrape() -> pd.DataFrame:
    """Scrape De Balie events and return as DataFrame."""
    df = retrieve()
    if len(df) == 0:
        logger.warning("No De Balie events found")
        return df
    df = post_process(df)
    logger.info(f"Scraped {len(df)} De Balie events")
    return df


def retrieve() -> pd.DataFrame:
    """Fetch events from De Balie WordPress API."""
    response = api_call()
    if response.status_code != 200:
        logger.warning(f"De Balie API returned status {response.status_code}")
        return pd.DataFrame()
    
    posts = response.json()
    
    # Filter for event-like posts (those with dates and URLs)
    events = []
    for post in posts:
        event = {
            'id': post.get('id'),
            'title': post.get('title', {}).get('rendered', ''),
            'link': post.get('link'),
            'date': post.get('date'),
        }
        if event['title']:
            events.append(event)
    
    df = pd.DataFrame(events)
    return df


 


def post_process(df: pd.DataFrame) -> pd.DataFrame:
    """Transform De Balie data to common schema."""
    df['start_date_time'] = pd.to_datetime(df['date'], errors='coerce')
    try:
        df['start_date_time'] = df['start_date_time'].dt.tz_localize('Europe/Amsterdam')
    except Exception:
        pass
    df = df.rename(columns={'title': 'title', 'link': 'ticket_url'})
    df['price'] = 15
    df['venue'] = 'De Balie'
    
    # include title column for mapping
    return df[['venue', 'start_date_time', 'ticket_url', 'price', 'title']]


def api_call() -> requests.Response:
    """Call De Balie API."""
    url = de_balie_config.BASE_URL + de_balie_config.API_ENDPOINT
    response = requests.get(url, headers=de_balie_config.HEADERS, params=de_balie_config.QUERY_PARAMS)
    return response
