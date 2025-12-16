"""Configuration for De Balie scraper."""

BASE_URL = "https://www.debalie.nl"
API_ENDPOINT = "/wp-json/wp/v2/posts"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
}

QUERY_PARAMS = {
    "per_page": 100
}
