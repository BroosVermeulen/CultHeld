"""Configuration for Melkweg scraper."""

BASE_URL = "https://www.melkweg.nl"
API_ENDPOINT = "/_next/data/{build_id}/nl/agenda.json"
WEBSITE_URL = "https://www.melkweg.nl/nl/agenda"

QUERY_PARAMS = {
    "slug": ["nl", "agenda"]
}

HEADERS = {
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Encoding": "gzip, deflate, br",
    "Purpose": "prefetch",
    "Sec-Fetch-Mode": "cors",
    "Accept-Language": "en-GB,en;q=0.9",
    "Host": "www.melkweg.nl",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    ),
    "Referer": "https://www.melkweg.nl/nl/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "x-nextjs-data": "1"
}

COOKIES = {
    "_ga_KFGKMS6566": "GS1.1.1691517649.1.1.1691517662.0.0.0",
    "_fbp": "fb.1.1691517650217.899090579",
    "_ga": "GA1.2.413805816.1691517650",
    "_gat_UA-40003495-1": "1",
    "_gid": "GA1.2.674701786.1691517650"
}

# Fallback build ID if auto-fetch fails (update as needed)
FALLBACK_BUILD_ID = "iMEO0fwvv6V7jsOgcjB4m"
