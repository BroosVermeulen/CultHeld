import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import datetime

def main():
    df = retrieve(str(datetime.date.today()), 10)
    df = post_process(df)

    return df


def post_process(df):
    df['price'] = 12

    return df


def retrieve(start_data, days):
    df_day = []
    for i in range(0, days):
        year = start_data.split('-')[0]
        month = start_data.split('-')[1]
        day = int(start_data.split('-')[2])+i
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        df_day.append(api_call(day, month, year))

    df = pd.concat(df_day)

    return df


def api_call(day, month, year):
    check_date = year + '-' + month + '-' + day

    url = "https://studio-k.nu/wp-admin/admin-ajax.php"

    payload = "action=loadShows&date="+check_date
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "studio-k.nu",
        "Origin": "https://studio-k.nu",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Connection": "keep-alive",
        "Referer": "https://studio-k.nu/films/",
        "Content-Length": "32",
        "Cookie": "_ga=GA1.2.326638887.1675445518; _gid=GA1.2.762247350.1675445518",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    json_data = json.loads(response.text)
    soup = BeautifulSoup(json_data['html'], features="html.parser")

    time = []
    for a in soup.find_all('a', attrs={'class':'time'}):
        mytime = datetime.datetime.strptime(a.contents[0],'%H:%M').time()
        myday = datetime.datetime(int(year), int(month), int(day))
        start_time = datetime.datetime.combine(myday, mytime)
        time.append(start_time)

    title = []
    link = []
    for a in soup.find_all('a', attrs={'class':'title'}):
        title.append(a.contents[0])
        link.append(a['href']) 

    df = pd.DataFrame({'start_date_time':time, 'title':title, 'ticket_url':link})

    return df
