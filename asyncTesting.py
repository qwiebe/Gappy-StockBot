import asyncio
import concurrent
from datetime import datetime
import pytz

from tradingfunctions import candles, currentPrice, placeOrder, cancelOrder, qtyPurchase
from private.config import account_num

###
# Considerations: possibly keeping track of the sum of selling volume in order to more accurately consider shorting
# To Do: Take care of case when no noticable correction occurs
###

# Setting time parameters
pattern = '%Y-%m-%dT%H:%M:%S%z'
easternTZ = pytz.timezone('US/Eastern')

# Truly Globally Awesome and Constraining (or not) Variables
purchase_counter = 0        # Note: may have to move this into the main async def and feed it to MakeMove

def waitForCorrection(ticker):
    triggerCandle = {}

    while True:
        # current time and appropriate candles
        currentTime = datetime.now(easternTZ).strftime(pattern)
        candleList = candles(ticker = ticker)
        currentCandle = candleList[0]
        priorCandle = candleList[1]

    # Check for red candle
        if currentCandle['open'] > currentCandle['close']: 
            # check if volume is due to shorting or just profit taking
            if currentCandle['volume'] < (priorCandle['volume'])/2:
                triggerCandle = triggerCandle.update(currentCandle)
                print('{}: Trigger set {}'.format(ticker, currentTime))
                break
            # only other case would be shorting of the stock... making it a 'no go'
            else:
                print('{} shorting at {}'.format(ticker, currentTime))
                triggerCandle = triggerCandle.update({'NoGood': 'Shorting'})
                break
    # return the trigger candle to the next function
    return triggerCandle


async def MakeMove(ticker):
    triggerCandle = await waitForCorrection(ticker)

    # This will change to true once a move has been made
    move_made = False

    #
    if 'NoGood' in triggerCandle:
        print('{}: Shorting occured'.format(ticker))
    else:
        while not(move_made):
            # Retrieve current time
            currentTime = datetime.now(easternTZ).strftime(pattern)

            # Retrieve candle and price info
            curPrice = currentPrice(ticker)['mark']     # retrieves market price of ticker
            priorCandle = candles(ticker)[1]
            currentCandle = candles(ticker)[0]

            # once again check for red candle and if the trigger should be moved up
            if currentCandle['open'] > currentCandle['close']:
                if currentCandle['high'] > triggerCandle['high']:
                    # check again if volume is due to shorting or just profit taking
                    if currentCandle['volume'] < (priorCandle['volume'])/2:
                        print('{}: New trigger changed from {} to {} {}'.format(ticker, triggerCandle['high'], currentCandle['high'], currentTime))
                        triggerCandle = currentCandle
                    # only other case would be shorting of the stock... making it a 'no go'
                    else:
                        print('{} shorting at {}'.format(ticker, currentTime))
                        triggerCandle = triggerCandle.update({'NoGood': 'Shorting'})

                    triggerCandle = currentCandle

            # Checks for beginning of potentially green candle
            elif curPrice > currentCandle['open']:
        # -------------------- MAKE THE PURCHASE --------------------        
            # note: this is the critical part. Current price must surpass the high of the trigger candle by at least 1cent 
                if curPrice > triggerCandle['high'] + 0.01:
                    order_qty, order_price, status_code = await qtyPurchase(account_num, ticker, purchase_counter)
                    stop_price = triggerCandle['low']
            
                    if status_code == 'REAL':
                        order_status, order_location = await placeOrder(ticker, order_price, order_qty, 'BUY', account_num, stop_price)
                        purchase_counter += 1
                        return order_qty, order_status, order_location, stop_price

                    #elif status_code == 'SIM':
                        #simulateOrder(ticker, marketprice, quantity)

async def ProfitAssurance(ticker, order_location, stop_price, order_qty):
    
    while True:
        # Check if position has been closed yet
        

        candleList = candles(ticker = ticker)
        priorCandle = candleList[1]
        priorLow = priorCandle['low']

        # Check if prior candle's low is > than the current stop loss price
        if priorLow > stop_price:
            placeOrder(ticker, priorLow, order_qty, 'STOP', account_num, -1)
            cancelOrder(order_location, account_num)
    

async def trade(ticker):
    # Pass to MakeMove
    order_qty, order_status, order_location, stop_price = await MakeMove(ticker)

    # Pass to ProfitAssurance which will change the Stop Loss/Close out the position
    await ProfitAssurance(ticker, order_location, stop_price, order_qty)



        # Next, pass to Profit Assurance
    
        # If move not made, pass to DayHighBreak

            # if move made, pass to Profit Assurance

async def main():
    # Locate Gappers
    gappers = await gappers()

    # Pass to trade()
    await asyncio.gather(trade(ticker) for ticker in gappers)


if __name__ == '__main__':
    asyncio.run(main)

print(f"{__file__} {__name__}")

    






'''
def get_chat_id(name):
    return "chat-%s" % name

async def main():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, get_chat_id, "django")
    print(result)

async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(main())

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()
'''