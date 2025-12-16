import json
import requests
import pandas as pd
from io import StringIO
from config import paradiso as paradiso_config
from utils.logging_config import get_logger

logger = get_logger(__name__)


def paradiso() -> pd.DataFrame:
    """Query Paradiso GraphQL API and return events as DataFrame."""
    url = paradiso_config.URL

    payload = {
        "query": paradiso_config.QUERY,
        "variables": paradiso_config.VARIABLES,
        "operationName": "programItemsQuery"
    }

    response = requests.request("POST", url, json=payload, headers=paradiso_config.HEADERS)

    json_data = json.loads(response.text)
    json_string = json.dumps(json_data['data']['program']['events'])

    df = pd.read_json(StringIO(json_string))
    logger.info(f"Scraped {len(df)} Paradiso events")

    return df
