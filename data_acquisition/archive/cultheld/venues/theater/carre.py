import requests
import json
import pandas as pd
import numpy as np
from flatten_json import flatten


def main():
    df = retrieve()
    df = post_process(df)

    return df


def post_process(df):
    # build start_date_time
    df = df.rename(columns={"start_date": "start_date_time"})
   
    # build title
    df = df.rename(columns={"name": "title"})

    # build price
    df['price'] = 50

    # build url
    df['ticket_url'] = df['sales_url']

    return df    


def retrieve():
    response = api_call()
    json_data = json.loads(response.text)

    all_events = []
    for x in json_data['productions']:
        all_events.append(json_data['productions'][x])

    json_string = json.dumps(all_events)
    df = pd.read_json(json_string)

    df = df.explode('events')
    df = df.dropna(subset=['events'])
    df_title = df["data"].apply(pd.Series)
    df_eventinformation = df["events"].apply(pd.Series)
    df = pd.concat([df_title, df_eventinformation], axis=1)

    return df


def api_call():
    url = "https://carre.nl/api/render/production-page-list-nl"

    payload = ""
    headers = {
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Dest": "empty",
        "Accept-Language": "en-GB,en;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Host": "carre.nl",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Referer": "https://carre.nl/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response
