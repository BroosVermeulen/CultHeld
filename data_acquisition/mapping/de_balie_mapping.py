from typing import Any


def map_de_balie(row: dict[str, Any]) -> dict[str, Any]:
    """Mapping function for De Balie scraper rows."""
    mapped = {}

    # Core ordered fields
    mapped['venue'] = 'De Balie'
    mapped['event_type'] = 'Actualiteit'
    mapped['event_name'] = row.get('title') or row.get('name')
    mapped['start_date_time'] = row.get('start_date_time')
    mapped['ticket_url'] = row.get('ticket_url')
    # Use extracted price if available, otherwise null
    mapped['price'] = row.get('price') if row.get('price') else None

    return mapped
