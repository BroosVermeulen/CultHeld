import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import datetime
from cultheld.constants import paths


START_DATE = str(datetime.date.today())
DAYS = 10

def retrieve_studiok(day, month, year):
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

df_day = []
for i in range(0, DAYS):
    year = START_DATE.split('-')[0]
    month = START_DATE.split('-')[1]
    day = int(START_DATE.split('-')[2])+i
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    check_date = year + '-' + month + '-' + day
    df_day.append(retrieve_studiok(day, month, year))

df = pd.concat(df_day)

df['type'] = 'Bioscoop'
df['venue'] = 'Studio K'
df['price'] = 12
df = df[['type', 'venue', 'start_date_time', 'title', 'price', 'ticket_url']]

df.to_csv(paths.OUTPUT + 'studiok.csv', encoding='utf-8')

