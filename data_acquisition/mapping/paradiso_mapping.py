def map_paradiso(row):
    """
    Mapping function for Paradiso scraper rows, replicating post_process.
    """
    mapped = {}

    # Add static venue name
    mapped['venue'] = 'Paradiso'

    # Prepend base URL
    mapped['ticket_url'] = 'http://www.paradiso.nl/' + row['uri'] if row.get('uri') else None

    # Rename startDateTime
    mapped['start_date_time'] = row.get('startDateTime')

    # Add price
    mapped['price'] = 30

    return mapped