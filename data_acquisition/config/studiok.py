"""Configuration for Studio K scraper."""

BASE_URL = "https://studio-k.nu"
API_ENDPOINT = "/wp-admin/admin-ajax.php"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "studio-k.nu",
    "Origin": "https://studio-k.nu",
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

QUERY_PARAMS = {}

# Number of days to fetch
DAYS_AHEAD = 10
