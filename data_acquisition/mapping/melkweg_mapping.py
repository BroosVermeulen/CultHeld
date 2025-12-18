from typing import Any


def map_melkweg(row: dict[str, Any]) -> dict[str, Any]:
    """
    Mapping function for Melkweg scraper rows, replicating post_process.
    """
    mapped = {}

    # Core ordered fields
    mapped['venue'] = 'Melkweg'
    mapped['event_type'] = 'Concert'
    mapped['event_name'] = row.get('title') or row.get('name') or row.get('summary')
    mapped['start_date_time'] = row.get('startDateTime') or row.get('startDate')
    ticket_path = row.get('uri') or row.get('url')
    mapped['ticket_url'] = f"http://www.melkweg.nl/{ticket_path}" if ticket_path else None
    # Use extracted price if available, otherwise null
    mapped['price'] = row.get('price') if row.get('price') else None

    return mapped
