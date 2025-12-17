# CultHeld Events Database Schema

## Core Events Table

The `events` table in `data/core/events.duckdb` stores all events from all venues.

### Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `venue` | VARCHAR | Yes | Venue name (e.g., 'Paradiso', 'Melkweg') |
| `event_name` | VARCHAR | No | Human-readable event title/name, if available |
| `start_date_time` | VARCHAR | Yes | Event start date/time in format "YYYY-MM-DD HH:mm" |
| `ticket_url` | VARCHAR | Yes | URL to purchase tickets |
| `price` | DECIMAL | Conditional | Ticket price (EUR). Required only for configured venues. |
| `as_of_date` | DATE | Yes | Date when record was scraped (ISO format YYYY-MM-DD) |

### Example Records

```
venue    | event_name                 | start_date_time   | ticket_url                              | price | as_of_date
---------|----------------------------|-------------------|------------------------------------------|-------|------------
Melkweg  | Artist X + Support         | 2025-12-20 21:00  | https://www.melkweg.nl/event/123         | 30    | 2025-12-16
Paradiso | Club Night Y               | 2025-12-21 20:30  | https://www.paradiso.nl/event/456        | null  | 2025-12-16
```

### Validation Rules

All records are validated before insertion:
- `venue`: Non-null, static value from mapper
- `start_date_time`: Non-null, must be valid datetime string
- `ticket_url`: Non-null, must be valid URL
- `price`: Conditionally required for a configurable set of venues. For other venues, `price` may be null when it cannot be reliably extracted.

Rows failing validation are logged and excluded from the database. The set of venues requiring price is defined in `config.PRICE_REQUIRED_VENUES`.

## Update Strategy

- **as_of_date**: Tracks when each record was scraped
- **Upsert**: Before inserting new records, all existing records for the same venue + as_of_date are deleted
- **Historical tracking**: Multiple as_of_dates are retained, allowing audit trails

## Query Examples

```sql
-- Get all events from Melkweg on 2025-12-16
SELECT * FROM events 
WHERE venue = 'Melkweg' AND as_of_date = '2025-12-16'
ORDER BY start_date_time;

-- Get latest events (most recent scrape per venue)
SELECT * FROM events 
WHERE as_of_date = (SELECT MAX(as_of_date) FROM events)
ORDER BY venue, start_date_time;

-- Count events by venue
SELECT venue, COUNT(*) as event_count 
FROM events 
WHERE as_of_date = CURRENT_DATE
GROUP BY venue;
```
