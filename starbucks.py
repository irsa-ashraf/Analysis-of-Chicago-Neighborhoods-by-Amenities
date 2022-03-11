API = "BcNrdvBLg1ZFWdTWKfTBxmu48ehAXPGM"

import requests
import pandas as pd
import json


def go():
    zips = ['60290', '60601', '60602', '60603', '60604', '60605', '60606', '60607', '60608', '60610', '60611', '60614',
        '60615', '60618', '60619', '60622', '60623', '60624', '60628', '60609', '60612', '60613', '60616', '60617',
        '60620', '60621', '60625', '60626', '60629', '60630', '60632', '60636', '60637', '60631', '60633', '60634',
        '60638', '60641', '60642', '60643', '60646', '60647', '60652', '60653', '60656', '60660', '60661', '60664', 
        '60639', '60640', '60644', '60645', '60649', '60651', '60654', '60655', '60657', '60659', '60666', '60668',
        '60673', '60677', '60669', '60670', '60674', '60675', '60678', '60680', '60681', '60682', '60686', '60687', 
        '60688', '60689', '60694', '60695', '60697', '60699', '60684', '60685', '60690', '60691', '60693', '60696',
        '60701']

    cafes = get_long_lat(zips)
    cafe_df = pd.DataFrame(cafes, columns=["address", "latitude", "long"])
    return cafe_df


def get_long_lat(zips):
    seen = set()
    cafe_lst = []
    for zipcode in zips:
        url = gen_url(zipcode)
        req = requests.get(url)
        data_json = json.loads(req.text)
        for cafe in data_json:
            one_cafe = []
            lat = cafe['lat']
            lon = cafe['lon']
            if (lat, lon) not in seen:
                address = format_location(cafe['display_name'])
                one_cafe.append(address) 
                one_cafe.append(cafe['lat'])
                one_cafe.append(cafe['lon'])
                cafe_lst.append(one_cafe)
            else:
                seen.add((lat, lon))
    return cafe_lst


def gen_url(zipcode):
    return f"http://open.mapquestapi.com/nominatim/v1/search.php?key={API}&format=json&q=starbucks+chicago+{zipcode}+[cafe]&addressdetails=1&limit=10"


def format_location(display_name):    
    split = display_name.split(',')
    if any(char.isdigit() for char in split[1]):
        name = split[2]
        idx = 2
    else:
        name = split[1]
        idx = 1
    return (name + ',' + split[idx + 1])