#Note: in this bot I have used taapi free API allowed one requestr every 15 second so I used bulk for performing multiple queire in on request.
#The work stock represent the crypto currency here.
#Import the requests library 
from ast import Or
import requests 
import schedule
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from datetime import datetime
import time
import ccxt
import config
import schedule
import pandas as pd
import csv
from pathlib import Path
import importlib 
import API.taapi
import time
import os.path
import time
importlib.reload(API.taapi)
NoOfGrids = 3
GridDifference = 50
indicator = [
	    {
		    "id": "movingAverage7",
	        "indicator": "ma",
			"optInTimePeriod":7
	    },
	    {
		    "id": "movingAverage25",
	        "indicator": "ma",
			"optInTimePeriod":25
	    }
]
#Below file papertrading purpose it contain the file object
csvfile=""
#writer contain the file write object
writer=""
#below is the current value of the stock
currentValue=0.0
#Below is the coin pair in which you want to make trades
orderCoinPair = "BTC/USDT"
#Set the API key for binance crypto exchange
exchange = ccxt.binanceus({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

def CreateCsvfile():
    global writer
    global csvfile
    if os.path.isfile('Dataset/MA7_MA25_Price_1minute.csv'):
        csvfile = open('MA7_MA25_Price_1minute.csv', 'w', newline='') 
        writer = csv.writer(csvfile, delimiter=',')
        print("File already exist continue with the already present file")
    else:
        with open('Dataset/MA7_MA25_Price_1minute.csv', 'w', newline='') as csvfile:
            fieldnames = ['MovingAverage7/USDT', 'MovingAverage25/USDT', 'BinancePriceBTC/USDT', 'Time/HH:MM:SS']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            print("Fill Successfully Created and Header Setted for that file.")
def RunBot():
    try:
        global currentValue
        global exchange
        global writer
        global csvfile
        obj1 = API.taapi.TaapiIndicator("binance","BTC/USDT","1m",indicator)
        obj1.SetIndicatorsValue()
        currentValue=exchange.fetch_ticker(orderCoinPair)["bid"]
        print("---------------Printing OBJ1-----------------------")
        with open('Dataset/MA7_MA25_Price_1minute.csv', 'a+', newline='') as csvfile:
            row=[obj1.result["data"][0]["result"]["value"], obj1.result["data"][1]["result"]["value"], currentValue, time.strftime("%H:%M:%S", time.localtime())]
            writer = csv.writer(csvfile)
            writer.writerow(row)
            print(row)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")

#-------------------------Program Compiler Starting point from coding point of view----------------------
#when it run for first time it will create csv file of file not already exist
CreateCsvfile()
# Run schdule every 15 seconds
schedule.every(15).seconds.do(RunBot)
#While loop execute again and again make the script active
while True:
    schedule.run_pending()
	#Sleep for for a seconds
    time.sleep(1)