# import the goods
import requests
import json
#from authorization import headers
from private.config import client_id

# list of indicies to look through
index_dict = {'DJIA': '$DJI',
              'Nasdaq_Comp': '$COMPX',
              'SP500': '$SPX.X'}



# ------------------------------ FUNCTIONS ------------------------------
# It is as it's named... returns whether the market is open today
def checkMarketHours(type = 'EQUITY'): # type = 'EQUITY' allows f() to be called w/o passing a param... essentially, default = 'EQUITY'
    url = r'https://api.tdameritrade.com/v1/marketdata/{}/hours'.format(type)

    # get market hour data and then parse json strig right away
    marketHours = requests.get(url, params = {'apikey': client_id}).json() # for Go Live, headers = headers
    
    if type == 'EQUITY':
        lowerType = 'equity'
        shortType = 'EQ'
    
    # isOpen tells whether the stock market will be open on that day
    isOpen = marketHours[lowerType][shortType]['isOpen']

    return isOpen

# Find movers based on TD API
def getMovers(index_ticker, direction, change_type):
    url = r'https://api.tdameritrade.com/v1/marketdata/{}/movers'.format(index_ticker)
    
    # establish payload
    payload = {'direction': direction,
               'change': change_type,
               'apikey': client_id}

    # returns json string with all the movers and their data
    moversReply = requests.get(url, params = payload) # when Go Live, set headers = headers

    # parse the json string
    movers = moversReply.json()

    return movers

# Makes a list of the top 10 movers from each of the indices based on direction (up/down) and change type (percent/value)
def listMovers(index_dict, direction, change_type):
    # establish list to dump movers into
    moverList = []

    # iterate over the index values
    for key in index_dict:
        print('Index: {}'.format(key))
        index_ticker = index_dict[key]
        print('Index Ticker: {}'.format(index_ticker))
        # use getMovers() to list movers on certain index
        moversOnIndex = getMovers(index_ticker, direction, change_type)
        # add movers to the list
        moverList.extend(moversOnIndex)
    return moverList

# Weed out for TD API movers
def weedOutMovers(unsortedList):
    sortedList = []
    for curTicker in unsortedList:
        
        # Handle Errors
        if 'error' in curTicker:
            print('ERROR: {}'.format(curTicker))
            break
        elif [] == curTicker:
            print('ERROR: Empty')
            continue

        curChange = curTicker['change']
        curVolume = curTicker['totalVolume']
        curPrice = curTicker['last']
        
        # set minimum volume
        if curVolume > 1000000 and curPrice < 100:
            # for initial ticker
            sortedList.append(curTicker)
                
    return sortedList

# -----------------------------------------------------------------------

# ------------------------ EXPORTABLE VARIABLES -------------------------
isMarketOpen = checkMarketHours()

if isMarketOpen:
    todaysUpMovers_raw = listMovers(index_dict,'up','percent')
    todaysUpMovers = weedOutMovers(todaysUpMovers_raw)
    print(todaysUpMovers)

# -----------------------------------------------------------------------