import requests
from authorization import headers, access_token
from config import account_num
from colorRef import colors
import math
############################################################
#   ToDo: - create function for simulation trading         #
#                                                          #
############################################################

# -------------------- GETTING DATA --------------------
# gets the candles for a particular ticker
def candles(ticker = 'TQQQ', periodType = 'day', period = '1', frequencyType = 'minute', frequency = '1', extHours = 'true'):
        
        url = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(ticker)

        payload = {'periodType': periodType,
                    'period': period,
                    'frequencyType': frequencyType,
                    'frequency': frequency,
                    'needExtendedHoursData': extHours}
        
        candles = requests.get(url, headers = headers, data = payload)

        return candles

# gets the current price for multiple tickers.  tickers = 'TQQQ' pr tickers = 'TQQQ, ERX, ...'
def currentPrices(tickers):
    url = r'https://api.tdameritrade.com/v1/marketdata/quotes'

    payload = {'symbol': tickers}

    prices = requests.get(url, headers = headers, params = payload).json()

    return prices
# gets the current price for a single ticker
def currentPrice(ticker):
    url = r'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(ticker)

    price = requests.get(url, headers = headers).json()

    return price[ticker]


# -------------------- PLACING ORDERS --------------------
# place various types of orders
def placeOrder(ticker, price, quantity, action, accountId): # action = 'BUY', 'SELL', 'STOP'
    url = r'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(accountId)
    if action == 'BUY' or action == 'SELL':
        payload = {'orderType': 'LIMIT', # may change this to 'MARKET'
                   'duration': 'GOOD_TILL_CANCEL',
                   'price': price,
                   'session': 'NORMAL',
                   'orderStrategyType': 'SINGLE',
                   'orderLegCollection': [{
                                        'instruction': action,
                                        'quantity': quantity,
                                        'instrument': {
                                                        'assetType': 'EQUITY',
                                                        'symbol': ticker
                                                        }
                                        }]
                }
    elif action == 'STOP':
        payload = {'session': 'NORMAL',
                   'duration': 'GOOD_TILL_CANCEL',
                   'orderType': 'STOP', # may change this to 'MARKET'
                   'stopPrice': price,
                   'stopType': 'STANDARD',
                   'orderStrategyType': 'SINGLE',
                   'orderLegCollection': [{
                                        'instruction': 'SELL',
                                        'quantity': quantity,
                                        'instrument': {
                                                        'assetType': 'EQUITY',
                                                        'symbol': ticker
                                                        }
                                        }]
                   }

    header = {'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'}

    order = requests.post(url = url, headers = header, json = payload)

    if order.status_code == 201:
        if action == 'BUY':
            print(colors.fg.green,'{} order for {} of {} has been placed at ${}'.format(action,quantity,ticker,price), colors.reset)
        elif action == 'SELL':
            print(colors.fg.red,'{} order for {} of {} has been placed at ${}'.format(action,quantity,ticker,price), colors.reset)
        else:
            print(colors.fg.yellow,'{} order for {} of {} has been placed at ${}'.format(action,quantity,ticker,price), colors.reset)
    else:
        print(order.status_code)
        print(order.json())
    return order.status_code

# simulation order... still needs to be finished
def fakeOrder(ticker, price, quantity, action):
    if action == 'BUY' or action == 'SELL':
        print('Something')
    elif action == 'STOP':
        print('Something Else')

# cancel order
def cancelOrder(orderId, accountId):
    url = r'https://api.tdameritrade.com/v1/accounts/{}/orders/{}'.format(accountId, orderId)

    cancel = requests.delete(url, headers = headers)

    print(cancel.status_code)

# DETERMINE WHAT QUANTITY TO PURCHASE
# Obtain account data
def acctData(accountId):
    url = r'https://api.tdameritrade.com/v1/accounts/{}'.format(accountId)

    payload = {'fields': 'positions,orders'}

    acct_data = requests.get(url, headers = headers, data = payload).json()

    return acct_data

# Determine quantity and price to purchase at
def qtyPurchase(accountId, ticker, purchase_counter):
    acct_data = acctData(accountId)
    # This will need to change if other accounts are added
    my_acct = acct_data['securitiesAccount']

    round_trips = my_acct['roundTrips']
    # Remaining purchases which can be made without going over PDT limit of 3 round trips per # days
    purchases_remaining = 3 - (purchase_counter+round_trips)
    
    # Never surpass 3 round trips
    if purchases_remaining > 0:
        cash_avail = my_acct['currentBalances']['cashAvailableForTrading']

        # Split cash evenly between the allotted num of purchases for the day
        investment = cash_avail/purchases_remaining
        
        # Market price of the stock
        cur_price = currentPrice(ticker)['mark']

        # Calculate number of shares to buy
        quantity = math.floor(investment/cur_price)

        # This status code is used to distinguish between actionable quantities vs simulation quantities
        status_code = 'REAL'
        return quantity, cur_price, status_code
    else:
        sim_qty = 100
        sim_price = currentPrice(ticker)['mark']
        status_code = 'SIM'
        return sim_qty, sim_price, status_code