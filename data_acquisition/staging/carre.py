from urllib.parse import unquote, urlparse

import pandas as pd

from utils.http_utils import safe_get, safe_json
from utils.logging_config import get_logger

logger = get_logger(__name__)


def _extract_slug(url: str) -> str:
    p = urlparse(url)
    path = p.path or url
    if '/voorstelling/' in path:
        slug = path.split('/voorstelling/')[-1].strip('/')
        return unquote(slug)
    return ''


def scrape() -> pd.DataFrame:
    """Scrape Carré by using the site's JSON API per production when possible,
    falling back to Playwright HTML rendering if needed.
    """
    events = []

    # Try Playwright to collect production URLs (if available).
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://carre.nl', wait_until='networkidle')
            hrefs = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
            browser.close()
    except Exception:
        logger.info(
            'Playwright not available when collecting Carré links; using static homepage fetch'
        )
        try:
            resp = safe_get('https://carre.nl')
            from bs4 import BeautifulSoup
            s = BeautifulSoup(resp.content, 'html.parser')
            hrefs = [a.get('href') for a in s.find_all('a', href=True)]
        except Exception as e:
            logger.error('Failed to fetch Carré homepage: %s', e)
            hrefs = []

    # Filter for production pages and limit volume
    ev_urls = [h for h in hrefs if h and '/voorstelling/' in h]
    # Normalize and dedupe
    seen = set()
    ev_urls_unique = []
    for h in ev_urls:
        if h not in seen:
            seen.add(h)
            ev_urls_unique.append(h)
        if len(ev_urls_unique) >= 100:
            break

    # For each production, try the API endpoint which returns structured events
    for full in ev_urls_unique:
        try:
            slug = _extract_slug(full)
            if not slug:
                continue
            api = f'https://carre.nl/api/render/voorstelling/{slug}'
            resp = safe_get(api)
            if resp.status_code != 200:
                logger.debug('Carré API %s returned %s', api, resp.status_code)
                continue
            data = safe_json(resp)
            productions = data.get('productions') or {}
            for prod_key, prod in productions.items():
                # try to get a production title from prod.data
                prod_data = prod.get('data') or {}
                prod_title = (
                    prod_data.get('title')
                    or prod_data.get('name')
                    or prod.get('id')
                    or slug
                )
                events_list = prod.get('events') or []
                for ev in events_list:
                    start = ev.get('start_date') or ev.get('start') or ev.get('start_date_time')
                    ticket = (
                        ev.get('sales_url')
                        or ev.get('ticketUrl')
                        or ev.get('salesUrl')
                        or ev.get('sales_url')
                    )
                    events.append({
                        'venue': 'Carré',
                        'start_date_time': start,
                        'ticket_url': ticket,
                        'price': '',
                        'title': prod_title,
                    })
        except Exception as e:
            logger.warning('Error fetching Carré production %s: %s', full, e)

    # If API yielded nothing, try a Playwright HTML parse per-production (older fallback)
    if not events:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page()
                for url in ev_urls_unique[:50]:
                    try:
                        page.goto(url, wait_until='networkidle')
                        content = page.content()
                        from bs4 import BeautifulSoup
                        s = BeautifulSoup(content, 'html.parser')
                        time_tag = s.find('time')
                        title_tag = s.find('h1')
                        start = None
                        if time_tag and time_tag.has_attr('datetime'):
                            start = time_tag['datetime']
                        title_text = title_tag.text.strip() if title_tag else url
                        events.append({
                            'venue': 'Carré',
                            'start_date_time': start,
                            'ticket_url': url,
                            'price': '',
                            'title': title_text,
                        })
                    except Exception as e:
                        logger.warning('Failed to parse Carré event %s: %s', url, e)
                browser.close()
        except Exception as e:
            logger.error('Playwright fallback failed for Carré: %s', e)

    df = pd.DataFrame(events)
    if not df.empty:
        # parse as UTC then convert to Amsterdam timezone
        df['start_date_time'] = pd.to_datetime(
            df['start_date_time'], errors='coerce', utc=True
        ).dt.tz_convert('Europe/Amsterdam')
        df = df.dropna(subset=['start_date_time'])
    return df

