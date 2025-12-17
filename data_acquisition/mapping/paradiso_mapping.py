from typing import Any


def map_paradiso(row: dict[str, Any]) -> dict[str, Any]:
    """
    Mapping function for Paradiso scraper rows, replicating post_process.
    """
    mapped = {}

    # Core ordered fields
    mapped['venue'] = 'Paradiso'
    mapped['event_name'] = row.get('title') or row.get('name') or row.get('summary')
    mapped['start_date_time'] = row.get('startDateTime')
    mapped['ticket_url'] = 'http://www.paradiso.nl/' + row['uri'] if row.get('uri') else None
    # Use extracted price if available, otherwise null
    mapped['price'] = row.get('price') if row.get('price') else None

    # Keep any additional fields (if needed) appended after
    return mapped