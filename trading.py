#
import time
import pytz
import requests
from datetime import datetime
#from authorization import headers
#from morning import isMarketOpen
#from tradingfunctions import *
#from gapscraper import tickers

#################################################################################
#   TO DO:  - Variables
#               
#               
#################################################################################

# Setting time parameters
pattern = '%Y-%m-%dT%H:%M:%S%z'
easternTZ = pytz.timezone('US/Eastern')

currentTime = datetime.now(easternTZ).strftime(pattern)

currentEpoch = int(time.mktime(time.strptime(currentTime, pattern)))

print(str(currentTime))


print(currentTime)
print(currentEpoch)

utc_dt = easternTZ.localize(datetime.utcfromtimestamp(1579584779))
print(utc_dt.strftime(pattern))



# -----------------------------------------------------------------------

test = [
    {
      "open": 98.5,
      "high": 98.609,
      "low": 98.49,
      "close": 98.609,
      "volume": 60186,
      "datetime": 1579608000000
    },
    {
      "open": 98.6,
      "high": 98.64,
      "low": 98.5,
      "close": 98.57,
      "volume": 30924,
      "datetime": 1579609800000
    },
    {
      "open": 98.57,
      "high": 98.77,
      "low": 98.51,
      "close": 98.7,
      "volume": 111877,
      "datetime": 1579611600000
    }]

print(test[0]['open'])

# ------------------------- WAIT FOR CORRECTION -------------------------

# This initial rendition will be for a single ticker
'''
currentPrice = currentPrices(ticker)
currentCandle = candles(ticker)[0]

if currentCandle
'''