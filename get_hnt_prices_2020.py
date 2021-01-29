import requests
import pandas as pd
from datetime import date, timedelta
import numpy as np
import time

headers = {}
payload = {}

end_day = date.fromisoformat('2020-12-31')
day_list_iso = []
for i in range(365):
    day = end_day - timedelta(days=i)
    iso = day.isoformat()
    day_list_iso.append(iso)

hnt_price_usd = []
for j in range(len(day_list_iso)):
    # coingecko price
    # rearrange date to DD-MM-YYYY
    date_str = day_list_iso[j]
    date_split = date_str.split('-')
    coingecko_date = date_split[2] + '-' + date_split[1] + '-' + date_split[0]
    url = "https://api.coingecko.com/api/v3/coins/helium/history?date=" + coingecko_date + "&localization=false"
    response = requests.request("GET", url, headers=headers, data=payload)

    i = 0
    while response.status_code == 429:
        print('Throttled, implementing backoff...')
        i += 1
        time.sleep(i)
        response = requests.request("GET", url, headers=headers, data=payload)
    prices = response.json()

    try:
        hnt_price_usd.append(prices['market_data']['current_price']['usd'])
    except KeyError:
        hnt_price_usd.append(hnt_price_usd[j - 1])
    if np.remainder(j, 10) == 0:
        print(day_list_iso[j])




df = pd.DataFrame(data=[day_list_iso, hnt_price_usd]).transpose()
df.columns = ['DATE', 'HNT_PRICE_USD']
df.to_csv('coingecko_prices_2020.csv')