"""Configuration for FCHYENA scraper."""

BASE_URL = "https://fchyena.nl"
API_ENDPOINT = "/json/shows.json"

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "en-GB,en;q=0.9",
    # Prefer identity to avoid automatic brotli/gzip payloads from some servers
    "Accept-Encoding": "identity",
    "Sec-Fetch-Mode": "cors",
    "Host": "fchyena.nl",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Referer": "https://fchyena.nl/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
}

QUERY_PARAMS = {}
