"""Configuration for Concertgebouw scraper."""

BASE_URL = "https://cms.concertgebouw.nl"
API_SEARCH_ENDPOINT = "/api/en/search.json"
API_PAGE_ENDPOINT = "/api/en/page.json"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
}

SEARCH_PARAMS = {
    "page": 1,
    "category.id": "concerts"
}

# Limit number of events to fetch (to avoid too many API calls)
EVENT_LIMIT = 250
