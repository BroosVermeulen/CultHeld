import re
from typing import Any


def map_carre(row: dict[str, Any]) -> dict[str, Any]:
    """Mapping function for Carré scraper rows."""
    mapped = {}

    # Core ordered fields
    mapped['venue'] = 'Carré'
    mapped['event_name'] = row.get('title') or row.get('name')
    mapped['start_date_time'] = row.get('start_date_time')
    mapped['ticket_url'] = row.get('ticket_url') or ''

    # normalize price to integer/float where possible, otherwise null
    price_raw = row.get('price')
    price_val = None
    if isinstance(price_raw, int | float):
        try:
            price_val = float(price_raw) if isinstance(price_raw, float) else int(price_raw)
        except Exception:
            price_val = None
    elif isinstance(price_raw, str) and price_raw.strip():
        m = re.search(r"([\d.]+)", price_raw.replace(',', '.'))
        if m:
            try:
                price_val = float(m.group(1))
            except Exception:
                price_val = None

    # Use parsed price or null
    mapped['price'] = price_val

    return mapped
