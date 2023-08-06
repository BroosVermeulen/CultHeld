''' Docstring TBF
'''
import json
import requests
import pandas as pd
from cultheld.constants import paths


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
        "gteStartDateTime": "2023-08-03",
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

df.to_csv(paths.OUTPUT + 'paradiso.csv', encoding='utf-8')

# url = "https://api.paradiso.nl/api/events"

# START_TIME = "2023-02-03 07:00:00"
# END_TIME = "2023-06-01 23:59:59"
# # START_TIME = "now"
# # END_TIME = "now"
# querystring = {"lang":"en","start_time":START_TIME,"end_time":END_TIME,"sort":"date","order":"asc","with":"images,locations"}

# payload = ""
# headers = {
#     "Accept": "application/json, text/javascript",
#     "Origin": "https://www.paradiso.nl",
#     "Access-Control-Max-Age": "1728000",
#     "Host": "api.paradiso.nl",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
#     "Accept-Language": "en-GB,en;q=0.9",
#     "Referer": "https://www.paradiso.nl/",
#     "Connection": "keep-alive"
# }

# response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
# json_data = json.loads(response.text)
# json_string = json.dumps(json_data)

# df = pd.read_json(json_string)
# # df = df[['title', 'ticket_url', 'ticket_price', 'ticket_currency', 'text', 'subtitle', 'status', 'start_date_time', 'start_date_presale', 'sold_out']]
# df['type'] = 'Concert'
# df = df.rename(columns={'ticket_price':'price'})
# df['venue'] = 'Paradiso'
# df = df[['type', 'venue', 'start_date_time', 'title', 'price', 'ticket_url']]
# df.to_csv('paradiso.csv', encoding='utf-8')
