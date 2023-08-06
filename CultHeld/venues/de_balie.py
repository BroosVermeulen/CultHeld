import requests
import json
import pandas as pd
import numpy as np


def main():
    df = retrieve()
    df = post_process(df)

    return df


def post_process(df):
    df_title = df[['id', 'title']].set_index('id')
    df_date = df['vo'].apply(pd.Series)
    df_date = df_date[['id', 'ticketLink', 'date', 'time']].set_index('id')
    df = df_title.join(df_date, how='outer')

    df['title'] = [d.get('rendered') for d in df.title]
    df['day'] = df['date'].str.split(' ').str[1].astype(int)
    df['day'] = np.where(
        df['day'] < 10, 
        '0' + df['day'].astype(str), 
        df['day'].astype(str)
    )
    df['month'] = df['date'].str.split(' ').str[2].map({
        'january':'01',
        'februari':'02',
        'maart':'03',
        'april':'04',
        'mei':'05',
        'juni':'06',
        'juli':'07',
        'augustus':'08',
        'september':'09',
        'oktober':'10',
        'november':'11',
        'december':'12'
    })
    df['year'] = df['date'].str.split(' ').str[3]
    df['start_date_time'] = pd.to_datetime(
        df['day'].astype(str) + "-" + df['month'].astype(str) + "-" + df['year'].astype(str) + " " + df['time'],
        format='%d-%m-%Y %H:%M'
    )

    df = df.rename(columns={'ticketLink':'ticket_url'})
    df['price'] = 10

    return df


def retrieve():
    collect_data = True
    page = 1
    df_page = []
    while collect_data == True:
        df = api_call(page)
        if 'code' in df.columns:
            if df['code'][0] == 'rest_post_invalid_page_number':
                break
        page = page + 1
        df_page.append(df)

    df = pd.concat(df_page)

    return df


def api_call(page):
    url = "https://debalie.nl/wp-json/wp/v2/vo-programme"

    querystring = {"_embed":"true","archive":"false","includeCinemaSpecials":"true","page":page,"vo-programme-category":"3,4,30,31,32,34,35,36,37,39,40,43,44,45,46,47,48,49"}

    payload = ""
    headers = {
        "Cookie": "_ga=GA1.1.1945833411.1675444510; _ga_1GX79CM85K=GS1.1.1675444509.1.1.1675444788.0.0.0; _fbp=fb.1.1675444516589.1827751286; _gid=GA1.2.1259541643.1675444510; wpgdprc-consent-4=1_required%2C2_required%2C3_accepted%2C4_required",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "debalie.nl",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Accept-Language": "en-GB,en;q=0.9",
        "Referer": "https://debalie.nl/",
        "Connection": "keep-alive"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    json_string = json.dumps(json_data)

    df = pd.read_json(json_string)

    return df
