from numpy.core.fromnumeric import size
from numpy.lib.function_base import append
import requests
import pandas as pd
import matplotlib
import os
import math
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import date
from datetime import datetime
from datetime import timedelta
import time

# API KEY
key = "PERSONAL KEY"
# URL FOR OPEN/CLOSE INFO
POLYGON_OC_URL = 'https://api.polygon.io/v1/open-close/{}/{}?adjusted=true&apiKey={}'
# TICKER LIST
TICKERS = ["AAPL", "MSFT", "AMZN", "FB", "GOOGL", "GOOG", "TSLA", "NVDA", "JPM", "JNJ", "V", "UNH", "PYPL", "HD", "PG", "MA", "DIS", "ADBE", "XOM", "NFLX", "VZ"]
#Date format for URL
DATE_FORMAT = "{}-{}-{}"

    

def getData(url = POLYGON_OC_URL):
    session = requests.Session()

    # loop through all stocks in TICKERS array
    for i in range(0, len(TICKERS)):

        # Set start date for each ticker
        start = "2019-07-29"
        curr_date = datetime.strptime(start, "%Y-%m-%d")

        # loop through all dates up until today    
        while(curr_date < datetime.today()):
            # ensure proper formatting on HTTP request
            str_month = str(curr_date.month)
            str_day = str(curr_date.day)
            zero_month = str_month.zfill(2)
            zero_day = str_day.zfill(2)

            # make API call
            r = session.get(POLYGON_OC_URL.format(TICKERS[i], DATE_FORMAT.format(curr_date.year, zero_month, zero_day), key))
            data = r.json()

            # if too many calls have been made, sleep for 60 seconds
            if(r.status_code == 429):
                time.sleep(60)
                r = session.get(POLYGON_OC_URL.format(TICKERS[i], DATE_FORMAT.format(curr_date.year, zero_month, zero_day), key))
                data = r.json()

           # error check to skip days when markets are closed
            while(r.status_code != 200 and curr_date < datetime.today()):
                curr_date = curr_date + timedelta(days= 1)

                # ensure proper formatting on HTTP request
                str_month = str(curr_date.month)
                str_day = str(curr_date.day)
                zero_month = str_month.zfill(2)
                zero_day = str_day.zfill(2)
                time.sleep(12)

                # API call
                r = session.get(POLYGON_OC_URL.format(TICKERS[i], DATE_FORMAT.format(curr_date.year, zero_month, zero_day), key))
                data = r.json()

                # if too many calls have been made, sleep for 60 seconds
                if(r.status_code == 429):
                    time.sleep(60)
                    r = session.get(POLYGON_OC_URL.format(TICKERS[i], DATE_FORMAT.format(curr_date.year, zero_month, zero_day), key))
                    data = r.json()

            

            # create DataFrame and move data to csv file
            if(curr_date < datetime.today()):
                df = pd.DataFrame(data= data, columns=[data["symbol"], data["close"], data["volume"], data["from"]])
                df.to_csv('data/data.csv', index= False, mode= "a")
                curr_date = curr_date + timedelta(days= 1)
                time.sleep(12)

        i += 1


getData()
