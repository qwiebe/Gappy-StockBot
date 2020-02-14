#
import time
import pytz
import requests
from datetime import datetime
#from authorization import headers
#from morning import isMarketOpen
from tradingfunctions import *
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
ticker = 'TQQQ'
# Variables independent of time
triggerCandle = {}
cash = acctData(account_num)['initialBalances']['cashAvailableForTrading'] # total cash available for the day


# Variables which change depending on time
currentPrice = currentPrices(ticker)
priorCandle = candles(ticker)[1]
currentCandle = candles(ticker)[0]

# Variables which change depending on action (buy, sell, other)
num_purchases = 0 # at the beginning of the day, the number of purchases made is none.  This is used so that you never go over the PDT limit


# Check for red candle
if currentCandle['open'] > currentCandle['close']: 
  # if trigger has not yet been set. i.e. only green candles in the morning
  if triggerCandle == {}:
    # check if volume is due to shorting or just profit taking
    if currentCandle['volume'] < (priorCandle['volume'])/2:
      triggerCandle = currentCandle
      print('{}: Trigger set {}'.format(ticker, currentTime))
    else:
      print('{} shorting at {}'.format(ticker, currentTime))
      #break
    # note: if the candles are updated live, this logic may need changing
    # if the current red candle is above the trigger candle, reset the trigger candle
  elif currentCandle['high'] > triggerCandle['high']:
    triggerCandle = currentCandle



# Won't do anything if a pull back/consolidation has not occured
if triggerCandle != {}:
  # Checks for beginning of potentially green candle
  if currentPrice > currentCandle['open']:
# -------------------- MAKE THE PURCHASE --------------------        
    # note: this is the critical part. Current price must surpass the high of the trigger candle by at least 1cent 
    if currentPrice > triggerCandle['high'] + 0.01:
      order_qty, order_price, status_code = qtyPurchase(account_num, ticker, num_purchases)
      
      if status_code == 'REAL':
        placeOrder(ticker, order_price, order_qty, 'BUY', account_num)
      #elif status_code == 'SIM':
        #simulateOrder(ticker, marketprice, quantity)