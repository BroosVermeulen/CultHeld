import json

import pandas as pd
import requests


def main():
    df = retrieve()
    df = post_process(df)

    return df


def post_process(df):
    # build start_date_time
    df = df.rename(columns={"eventDate": "start_date_time"})
   
    # build title
    df = df.rename(columns={"name": "title"})

    # build price
    df['price'] = df['minPrice']

    # build url
    df['ticket_url'] = df['url']

    return df


def retrieve():
    response = api_call_1()
    json_data = json.loads(response.text)
    
    i = 0
    json_data_all_events = []
    for x in json_data['data']['events']['hits']:
        if i > 250: break  # NEEDS TO BE REMOVED
        i+=1

        response = api_call_2(x['uri'])
        json_data = json.loads(response.text)
        json_data_all_events.append(json_data)
        
    json_string = json.dumps(json_data_all_events)
    df = pd.read_json(json_string)

    return df


def api_call_2(event):
    url = "https://cms.concertgebouw.nl/api/en/page.json"

    querystring = {"url":""+event}

    payload = ""
    headers = {
        "Sec-Fetch-Site": "same-site",
        "Accept": "*/*",
        "Origin": "https://www.concertgebouw.nl",
        "Sec-Fetch-Dest": "empty",
        "Accept-Language": "en-GB,en;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Host": "cms.concertgebouw.nl",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Referer": "https://www.concertgebouw.nl/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return response


def api_call_1():
    url = "https://cms.concertgebouw.nl/api"

    payload = {
        "query": "query searchEvents($site:[String], $eventEndDate:[String], $keyword:String, $composers:[String], $discounts:[String], $genres:[String], $importIconcertStatus: [String], $instruments:[String], $rooms:[String], $specials:[String], $tags:[String]) { \
            events: elasticSearch(site:$site, section:\"event\", fuzzyness:\"0\", eventEndDateRange:$eventEndDate, search:$keyword, composersFacet:$composers, importDiscountGroupsFacet:$discounts, genresFacet:$genres, importIconcertStatusFacet: $importIconcertStatus, instrumentsFacet:$instruments, roomFacet:$rooms, specialsFacet:$specials, tagsFacet:$tags, orderBy:\"eventDate ASC\") { \
                facets(limit:1024) { \
                composers { label: value, count } \
                discounts: importDiscountGroups { value, count } \
                genres { label: value, count } \
                instruments { label: value, count } \
                rooms: room { label: value, count } \
                specials { label: value, count } \
                } \
                count \
                hits(limit:1024) { \
                uri \
                } \
            } \
            topEvents: elasticSearch(site:$site, section:\"event\", eventEndDateRange:$eventEndDate, search:$keyword, composersFacet:$composers, importDiscountGroupsFacet:$discounts, genresFacet:$genres, importIconcertStatusFacet: $importIconcertStatus, instrumentsFacet:$instruments, roomFacet:$rooms, specialsFacet:$specials, tagsFacet:$tags) { \
                hits(limit:5) { \
                uri \
                } \
            } \
            }",
        "variables": {
            "site": "enDefault",
            "eventEndDate": "gte 2023-08-08T00:00:00.000Z",
            "keyword": "",
            "composers": [],
            "discounts": [],
            "genres": [],
            "importIconcertStatus": ["1e Optie", "Bevestigd", "Contract uit", "Corona", "Voor brochure", "Verplaatst", "Geannuleerd"],
            "instruments": [],
            "rooms": [],
            "specials": [],
            "tags": []
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer SVNNqbdCSqwqNVTmFbXEPJbN6MC6axVi",
        "Sec-Fetch-Site": "same-site",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Host": "cms.concertgebouw.nl",
        "Origin": "https://www.concertgebouw.nl",
        "Content-Length": "1833",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Referer": "https://www.concertgebouw.nl/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response
