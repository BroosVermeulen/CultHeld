import json
import requests
import pandas as pd
from datetime import datetime


def main():
    #df = retrieve(str(datetime.date.today()), 10)
    #df = post_process(df)

    df = retrieve()
    df = post_process(df)

    return df


def post_process(df):
    # build start_date_time
    df['month'] = df['date_start'].str.slice(0, 2)
    df['day'] = df['date_start'].str.slice(2, 4)
    df['year'] = datetime.now().year
    df['start_date_time'] = pd.to_datetime(
        df['day'].astype(str) + "-" + df['month'].astype(str) + "-" + df['year'].astype(str) + " " + df['time_start'],
        format='%d-%m-%Y %H:%M'
    )

    # build title
    df = df.rename(columns={"name": "title"})

    # build price
    df['price'] = 10

    # build url
    df['ticket_url'] = 'TBD'

    return df


def api_call():
    url = "https://fchyena.nl/json/shows.json"

    querystring = {"t":"1691514480000"}

    payload = ""
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Host": "fchyena.nl",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Connection": "keep-alive",
        "Referer": "https://fchyena.nl/nieuws",
        "Cookie": "CraftSessionId=decfc4fd8a10b9ecb0f85a1a9ea9ac0c",
        "Sec-Fetch-Dest": "empty",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return response


def retrieve():
    response = api_call()

    json_data = json.loads(response.text)
    out = []
    for x in json_data['movies']:
        for y in json_data['movies'][x]:
            out.append(y)
    json_string = json.dumps(out)

    df = pd.read_json(json_string, dtype={'date_start': str})

    return df
