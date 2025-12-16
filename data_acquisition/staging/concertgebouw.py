import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
from utils.logging_config import get_logger
from utils.http_utils import safe_get, safe_json

logger = get_logger(__name__)


def concertgebouw(max_events: int = 50) -> pd.DataFrame:
    """Scrape Concertgebouw events by harvesting event links and parsing pages."""
    base = 'https://www.concertgebouw.nl'
    listing = safe_get(base + '/en/concerts-and-tickets')
    try:
        soup = BeautifulSoup(listing.content, 'html.parser')
    except Exception as e:
        logger.error('Failed to parse Concertgebouw listing: %s', e)
        return pd.DataFrame(columns=['venue', 'start_date_time', 'ticket_url', 'price'])

    links = [a['href'] for a in soup.find_all('a', href=True)]
    ev_links = [h for h in links if h.startswith('/en/concerts/')]
    # dedupe
    seen = set()
    unique = []
    for h in ev_links:
        if h not in seen:
            seen.add(h)
            unique.append(h)
        if len(unique) >= max_events:
            break

    events = []
    for rel in unique:
        url = base + rel
        try:
            resp = safe_get(url)
            page = BeautifulSoup(resp.content, 'html.parser')
            # try JSON-LD first
            jl = page.find('script', type='application/ld+json')
            start_dt = None
            ticket_url = None
            if jl and (jl.string or jl.text):
                try:
                    import json
                    data = json.loads(jl.string or jl.text)
                    # data may be dict with startDate or offers
                    if isinstance(data, dict):
                        start_dt = data.get('startDate') or data.get('start_date')
                        offers = data.get('offers')
                        if isinstance(offers, dict):
                            ticket_url = offers.get('url')
                except Exception:
                    pass

            # fallback to HTML parsing
            if not start_dt:
                time_tag = page.find('time')
                if time_tag:
                    start_dt = time_tag.get('datetime') or time_tag.text.strip()
            title_tag = page.find('h1')
            title = title_tag.text.strip() if title_tag else rel
            # fallback ticket link
            if not ticket_url:
                a_ticket = page.find('a', href=lambda x: x and ('tix.concertgebouw.nl' in x or 'tickets' in x or 'buy' in x))
                if a_ticket:
                    ticket_url = a_ticket.get('href')

            # Ensure required fields are present (validation requires non-null values)
            if not ticket_url:
                ticket_url = url

            # try to extract a price from JSON-LD offers if available
            price_val = ''
            if jl and (jl.string or jl.text):
                try:
                    import json
                    data = json.loads(jl.string or jl.text)
                    offers = None
                    if isinstance(data, dict):
                        offers = data.get('offers')
                    # offers might be a dict or a list
                    if isinstance(offers, dict):
                        price_val = offers.get('price') or offers.get('priceSpecification', {}).get('price') or ''
                    elif isinstance(offers, list) and offers:
                        price_val = offers[0].get('price') or offers[0].get('priceSpecification', {}).get('price') or ''
                except Exception:
                    price_val = ''

            events.append({'venue': 'Concertgebouw', 'start_date_time': start_dt, 'ticket_url': ticket_url, 'price': price_val, 'title': title})
        except Exception as e:
            logger.warning('Failed to fetch Concertgebouw event %s: %s', rel, e)

    df = pd.DataFrame(events)
    # normalize start_date_time
    if not df.empty:
        # parse as UTC then convert to Amsterdam timezone
        df['start_date_time'] = pd.to_datetime(df['start_date_time'], errors='coerce', utc=True).dt.tz_convert('Europe/Amsterdam')
        df = df.dropna(subset=['start_date_time'])
    return df

