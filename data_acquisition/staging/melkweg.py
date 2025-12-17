import json
import re
from io import StringIO

import pandas as pd
import requests

from config import melkweg as melkweg_config
from utils.logging_config import get_logger

logger = get_logger(__name__)


def _get_melkweg_build_id() -> str:
    """Fetch the current Next.js build ID from Melkweg website."""
    try:
        response = requests.get(melkweg_config.WEBSITE_URL, timeout=10)
        match = re.search(r'"buildId":"([^"]+)"', response.text)
        if match:
            build_id = match.group(1)
            logger.info(f"Fetched Melkweg build ID: {build_id}")
            return build_id
    except Exception as e:
        logger.warning(f"Failed to fetch build ID: {e}. Using fallback.")
    return melkweg_config.FALLBACK_BUILD_ID


def scrape() -> pd.DataFrame:
    """Scrape Melkweg events from API and return as DataFrame."""
    response = api_call()
    json_data = json.loads(response.text)
    out = []
    for x in json_data['pageProps']['pageData']['attributes']['content'][0]['attributes']['initialEvents']:
        out.append(x['attributes'])
    json_string = json.dumps(out)

    df = pd.read_json(StringIO(json_string))
    logger.info(f"Scraped {len(df)} Melkweg events")

    return df


def api_call() -> requests.Response:
    """Call Melkweg API with current build ID."""
    build_id = _get_melkweg_build_id()
    url = f"https://www.melkweg.nl{melkweg_config.API_ENDPOINT}".format(build_id=build_id)

    payload = ""
    response = requests.request("GET", url, data=payload, headers=melkweg_config.HEADERS, params=melkweg_config.QUERY_PARAMS)

    return response
