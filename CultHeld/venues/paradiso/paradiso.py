''' Docstring TBF
'''
import json
import requests
import pandas as pd

from constants.paths import PARADISO_DATA


url = "https://api.paradiso.nl/api/events"

START_TIME = "2023-01-01 07:00:00"
END_TIME = "2023-06-01 23:59:59"
# START_TIME = "now"
# END_TIME = "now"
querystring = {"lang":"en","start_time":START_TIME,"end_time":END_TIME,"sort":"date","order":"asc","with":"images,locations"}

payload = ""
headers = {
    "Accept": "application/json, text/javascript",
    "Origin": "https://www.paradiso.nl",
    "Access-Control-Max-Age": "1728000",
    "Host": "api.paradiso.nl",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.paradiso.nl/",
    "Connection": "keep-alive"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
json_data = json.loads(response.text)
json_string = json.dumps(json_data)

df = pd.read_json(json_string)
df = df[['title', 'ticket_url', 'ticket_price', 'ticket_currency', 'text', 'subtitle', 'status', 'start_date_time', 'start_date_presale', 'sold_out']]
df.to_csv(PARADISO_DATA, encoding='utf-8')
