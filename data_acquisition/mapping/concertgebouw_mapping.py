from typing import Any


def map_concertgebouw(row: dict[str, Any]) -> dict[str, Any]:
    """Mapping function for Concertgebouw scraper rows."""
    mapped = {}

    # Core ordered fields
    mapped['venue'] = 'Concertgebouw'
    mapped['event_name'] = row.get('title') or row.get('name')
    mapped['start_date_time'] = row.get('start_date_time')
    mapped['ticket_url'] = row.get('ticket_url')
    # Try to parse extracted price as float, otherwise null
    price_val = row.get('price')
    try:
        if price_val and isinstance(price_val, str):
            mapped['price'] = float(price_val)
        elif price_val:
            mapped['price'] = float(price_val)
        else:
            mapped['price'] = None
    except (ValueError, TypeError):
        mapped['price'] = None

    return mapped
