from datetime import datetime

import pandas as pd

from config import fchyena as fchyena_config
from utils.http_utils import safe_get, safe_json
from utils.logging_config import get_logger

logger = get_logger(__name__)


def scrape() -> pd.DataFrame:
    """Scrape FCHYENA events and return as DataFrame using robust HTTP utils."""
    try:
        resp = safe_get(fchyena_config.BASE_URL + fchyena_config.API_ENDPOINT, headers=fchyena_config.HEADERS, params=fchyena_config.QUERY_PARAMS)
    except Exception as e:
        logger.error("FCHYENA HTTP request failed: %s", e)
        return pd.DataFrame(columns=['start_date_time', 'ticket_url', 'price'])

    try:
        data = safe_json(resp)
    except Exception:
        logger.warning("FCHYENA JSON parse failed, attempting HTML fallback")
        # HTML fallback: try to fetch homepage/agenda and parse times
        try:
            html_resp = safe_get(fchyena_config.BASE_URL)
            return _parse_shows_from_html(html_resp.content)
        except Exception as e:
            logger.error("FCHYENA HTML fallback failed: %s", e)
            return pd.DataFrame(columns=['start_date_time', 'ticket_url', 'price'])

    # Expecting {'status': str, 'movies': {movie_id: [shows]}}
    movies = data.get('movies') if isinstance(data, dict) else None
    if not movies:
        logger.warning("FCHYENA response missing 'movies' key or empty; attempting HTML fallback")
        try:
            html_resp = safe_get(fchyena_config.BASE_URL)
            return _parse_shows_from_html(html_resp.content)
        except Exception as e:
            logger.error("FCHYENA HTML fallback failed: %s", e)
            return pd.DataFrame(columns=['start_date_time', 'ticket_url', 'price'])

    events = []
    for movie_id, shows in movies.items():
        if isinstance(shows, list):
            for show in shows:
                date_start = show.get('date_start', '')
                time_start = show.get('time_start', '00:00')
                # date_start in format MMDD
                if len(date_start) == 4:
                    month = date_start[:2]
                    day = date_start[2:4]
                    year = datetime.now().year
                    try:
                        # parse as localized Amsterdam time
                        start_dt = pd.to_datetime(f"{day}-{month}-{year} {time_start}", format="%d-%m-%Y %H:%M")
                        # localize naive dt to Europe/Amsterdam
                        try:
                            start_dt = start_dt.tz_localize('Europe/Amsterdam')
                        except Exception:
                            pass
                    except Exception:
                        start_dt = None
                else:
                    start_dt = None

                events.append({
                    'start_date_time': start_dt,
                    'ticket_url': 'https://fchyena.nl',
                    'price': 10,
                })

    df = pd.DataFrame(events)
    # Drop rows without start_date_time
    df = df.dropna(subset=['start_date_time'])
    return df


def _parse_shows_from_html(html: bytes) -> pd.DataFrame:
    """Parse the FCHYENA site HTML and attempt to extract show datetimes and ticket links.

    This is a forgiving parser: it looks for <time datetime="..."> tags and nearby anchors.
    """
    try:
        from bs4 import BeautifulSoup
    except Exception:
        logger.error('bs4 not installed; cannot run HTML fallback')
        return pd.DataFrame(columns=['start_date_time', 'ticket_url', 'price'])

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        logger.error('Failed to parse FCHYENA HTML: %s', e)
        return pd.DataFrame(columns=['start_date_time', 'ticket_url', 'price'])

    events = []
    # Find time tags first
    for time_tag in soup.find_all('time'):
        dt = None
        try:
            if time_tag.has_attr('datetime'):
                dt = time_tag['datetime']
            else:
                dt = time_tag.text.strip()
            # try to parse and coerce to Amsterdam timezone
            start_dt = pd.to_datetime(dt, errors='coerce')
            try:
                if start_dt.tzinfo is None:
                    start_dt = start_dt.tz_localize('Europe/Amsterdam')
                else:
                    start_dt = start_dt.tz_convert('Europe/Amsterdam')
            except Exception:
                pass
            # if parsing failed and dt has no year, try appending current year
            import re
            if (start_dt is None or pd.isna(start_dt)) and dt and not re.search(r"\b\d{4}\b", dt):
                from datetime import datetime as _dt
                try:
                    start_dt = pd.to_datetime(f"{dt} {_dt.now().year}", dayfirst=True, errors='coerce')
                    try:
                        if start_dt.tzinfo is None:
                            start_dt = start_dt.tz_localize('Europe/Amsterdam')
                        else:
                            start_dt = start_dt.tz_convert('Europe/Amsterdam')
                    except Exception:
                        pass
                except Exception:
                    start_dt = None
        except Exception:
            start_dt = None

        # find nearest anchor (parent or next sibling)
        ticket = None
        parent = time_tag.parent
        if parent:
            a = parent.find('a', href=True)
            if a:
                ticket = a['href']

        if not ticket:
            # try following siblings
            sib = time_tag.find_next('a')
            if sib and sib.has_attr('href'):
                ticket = sib['href']

        if start_dt is not None and not pd.isna(start_dt):
            events.append({'start_date_time': start_dt, 'ticket_url': ticket or fchyena_config.BASE_URL, 'price': 10})

    df = pd.DataFrame(events)
    return df


 

