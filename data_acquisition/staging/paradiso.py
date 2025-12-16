import json
import requests
import pandas as pd


def paradiso():
    url = "https://gqlcache-production.paradiso.workers.dev/graphql"

    payload = {
        "query": " \
    query programItemsQuery( \
        $site: String \
        $size: Int = 100 \
        $gteStartDateTime: DateTime \
        $lteStartDateTime: DateTime \
        $searchAfter: [String] \
        $location: [Int] \
        $subBrand: [Int] \
        $contentCategory: [Int] \
        $highlight: Boolean = false \
    ) { \
        program( \
        site: $site \
        size: $size \
        gteStartDateTime: $gteStartDateTime \
        lteStartDateTime: $lteStartDateTime \
        searchAfter: $searchAfter \
        location: $location \
        subBrand: $subBrand \
        contentCategory: $contentCategory \
        highlight: $highlight \
        ) { \
        __typename \
        events { \
            __typename \
            id \
            uri \
            title \
            startDateTime @formatDateTime(format: \"Y-m-d H:i\", timezone: \"Europe/Amsterdam\") \
            date @formatDateTime(format: \"Y-m-d H:i\", timezone: \"Europe/Amsterdam\") \
            subtitle \
            price \
            sort \
            eventStatus \
            highlight \
            supportAct \
            announceSupport \
            soldOut \
            location { \
            id \
            title \
            } \
            image { \
            desktop \
            } \
        } \
        } \
    } \
    ",
        "variables": {
            "site": "paradisoEnglish",
            "size": 50,
            "gteStartDateTime": "2025-12-15",
            "lteStartDateTime": None,
            "searchAfter": None,
            "location": None,
            "subBrand": None,
            "contentCategory": None
        },
        "operationName": "programItemsQuery"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Authorization": "Bearer qNG1MfNixLtJU_iE_nvJ3ssmMY5NZ3Nx",
        "Sec-Fetch-Site": "cross-site",
        "Accept-Language": "en-GB,en;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Host": "gqlcache-production.paradiso.workers.dev",
        "Origin": "https://www.paradiso.nl",
        "Content-Length": "1787",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Referer": "https://www.paradiso.nl/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Priority": "u=3, i"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    json_data = json.loads(response.text)
    json_string = json.dumps(json_data['data']['program']['events'])

    df = pd.read_json(json_string)

    return df
