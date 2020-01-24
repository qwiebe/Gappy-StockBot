import requests
from authorization import headers, access_token
from config import account_num
from colorRef import colors

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

    prices = requests.get(url, headers = headers, data = payload)

    return prices

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
    
# cancel order
def cancelOrder(orderId, accountId):
    url = r'https://api.tdameritrade.com/v1/accounts/{}/orders/{}'.format(accountId, orderId)

    cancel = requests.delete(url, headers = headers)

    print(cancel.status_code)