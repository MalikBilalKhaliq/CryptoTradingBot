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
from datetime import datetime
importlib.reload(API.taapi)

noOfGrids = 3
gridDifference = 50

gridInstance = '{"instance":['
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
tradeAmmountUSDT= 50
tradeAmmountBTC= float(tradeAmmountUSDT/exchange.fetch_ticker(orderCoinPair)["bid"])
def CreateCsvfile():
    global writer
    global csvfile
    if os.path.isfile('Dataset/MA7_MA25_Trading_1min.csv'):
        csvfile = open('MA7_MA25_Trading_1min.csv', 'w', newline='') 
        writer = csv.writer(csvfile, delimiter=',')
        print("File already exist continue with the already present file")
    else:
        with open('Dataset/MA7_MA25_Trading_1min.csv', 'w', newline='') as csvfile:
            fieldnames = ['GridValue', 'BuyTimeMA7/USDT','BuyTimeMA25/USDT', 'SellTimeMA7/USDT', 'SellTimeMA25/USDT','BTCAmmountBuying', 'BuyTimePriceBinanceBTC/USDT','SellTimePriceBinanceBTC/USDT', 'Profit/USDT', 'BuyDateAndTime', 'SellDateAndTime']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            print("Fill Successfully Created and Header Setted for that file.")

def setGridInstances():
    global gridInstance
    global noOfGrids
    for i in range(noOfGrids): 
        if i==noOfGrids-1:
            gridInstance += '{}'
        else:
            gridInstance += '{},'
    gridInstance += ']}'
    gridInstance = eval(gridInstance)    
    for i in range(noOfGrids):
        print("Value Of I")
        print(i)
        gridInstance["instance"][i]["value"] = ((i+1) * 50) * -1
        gridInstance["instance"][i]["status"] = False
        gridInstance["instance"][i]["buytimeMA7"] = 0
        gridInstance["instance"][i]["selltimeMA7"] = 0
        gridInstance["instance"][i]["buytimeMA25"] = 0
        gridInstance["instance"][i]["selltimeMA25"] = 0
        gridInstance["instance"][i]["BTCammountbuying"] = 0
        gridInstance["instance"][i]["buytimepriceBinanceBTC/USDT"] = 0
        gridInstance["instance"][i]["selltimepricebinanceBTC/USDT"] = 0
        gridInstance["instance"][i]["selldateandtime"] = 0

def executeTrade(gridNo):
    now = datetime.now()
    print("-------------------Executing Grid No %d Order-----------------",(gridNo))
    gridInstance["instance"][gridNo]["buytimeMA7"] = obj1.result["data"][0]["result"]["value"]
    gridInstance["instance"][gridNo]["buytimeMA25"] = obj1.result["data"][1]["result"]["value"]
    gridInstance["instance"][gridNo]["BTCammountbuying"] = tradeAmmountBTC
    gridInstance["instance"][gridNo]["buytimepriceBinanceBTC/USDT"] = exchange.fetch_ticker(orderCoinPair)["bid"]
    gridInstance["instance"][gridNo]["buydateandtime"] = now.strftime("%d/%m/%Y %H:%M:%S")
    gridInstance["instance"][gridNo]["status"] = True
    print(gridInstance["instance"][gridNo])

def endTrade(gridNo):
    print("-------------------Ending Grid No %d Order-----------------",(gridNo))
    with open('Dataset/MA7_MA25_Trading_1min.csv', 'a+', newline='') as csvfile:
        currentBTCUSDTprice = exchange.fetch_ticker(orderCoinPair)["bid"]
        currentProfitUSDT = float(float(currentBTCUSDTprice * tradeAmmountBTC ) - float(gridInstance["instance"][gridNo]["buytimepriceBinanceBTC/USDT"] * tradeAmmountBTC))
        now = datetime.now()
        row=[gridInstance["instance"][gridNo]["value"], gridInstance["instance"][gridNo]["buytimeMA7"], gridInstance["instance"][gridNo]["buytimeMA25"], obj1.result["data"][0]["result"]["value"], obj1.result["data"][1]["result"]["value"], tradeAmmountBTC, gridInstance["instance"][gridNo]["buytimepriceBinanceBTC/USDT"], currentBTCUSDTprice , currentProfitUSDT, now.strftime("%d/%m/%Y %H:%M:%S") ]
        gridInstance["instance"][gridNo]["status"] = False
        writer = csv.writer(csvfile)
        writer.writerow(row)
        print("Order Grid No %d Successfully sold and Logged", gridNo)
        print(row)  
    

def ApplyStrategy():
    global gridInstance
    ma7=obj1.result["data"][0]["result"]["value"]
    ma25=obj1.result["data"][1]["result"]["value"]

    print("Current Status of the difference %d", ma7-ma25)
    #
    if not gridInstance["instance"][0]["status"]:
        if (ma7-ma25)<= gridInstance["instance"][0]["value"]:
            executeTrade(0)    
    elif not gridInstance["instance"][1]["status"]:
        if (ma7-ma25)<= gridInstance["instance"][1]["value"]:
            executeTrade(1)  
    elif not gridInstance["instance"][2]["status"]:
        if (ma7-ma25)<= gridInstance["instance"][2]["value"]:
            executeTrade(2)  

    if  gridInstance["instance"][0]["status"]:
        if (ma7-ma25) >= (gridInstance["instance"][0]["value"] + gridDifference ):
            endTrade(0)          
    elif gridInstance["instance"][1]["status"]:
        if (ma7-ma25) >= (gridInstance["instance"][1]["value"] + gridDifference ):
            endTrade(1) 
    elif gridInstance["instance"][2]["status"]:
        if (ma7-ma25) >= (gridInstance["instance"][2]["value"] + gridDifference ):
            endTrade(2) 

def RunBot():
    try:
        global currentValue
        global exchange
        global writer
        global csvfile
        global gridInstance
        global obj1
        obj1 = API.taapi.TaapiIndicator("binance","BTC/USDT","1m",indicator)
        obj1.SetIndicatorsValue()
        print(obj1.result)
        ApplyStrategy()
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")

#-------------------------Program Compiler Starting point from coding point of view----------------------
#when it run for first time it will create csv file of file not already exist
CreateCsvfile()
# Run schdule every 15 seconds
setGridInstances()
schedule.every(15).seconds.do(RunBot)
#While loop execute again and again make the script active
while True:
    schedule.run_pending()
	#Sleep for for a seconds
    time.sleep(1)