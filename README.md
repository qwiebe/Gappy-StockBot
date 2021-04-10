# Gappy
This is a README

Have you read it?
If not, please do so.

If you have read this line but not the ones below, please read the lines below.
If you have read all the lines, thank you!

## About This Project
The intent of this project is to explore the potential of **algorithmic trading**.  Written in python, Gappy takes advantage of TD Ameritrade's API in order to make trades on the behalf of the account holder.  The current in-progress algorithm identifies a selection of stock tickers which have gapped-up in the pre-market hours (hence Gappy!).  Then, those tickers are monitored and a buy-order will be sent if the following criteria are fulfilled.

### Buying
1. The first correction has taken place.  (a stock may gap-up, but at some point there has to be some consolidation where the first-movers dump their early morning quick profits.  After this point, the stock is less volatile; and, if the following conditions are met, it has a higher chance of maintaining an upward trend on which we can capitalize)
  - This first correction (represented by a red candle) is referred to as the _trigger candle_
  - **Correction must not be confused with shorting!**  If the volume of the current red candle is less than the volume of the prior green candle (or less than half than the prior candle in general), it's semi-safe to assume the volume is due to profit-taking (correction) and not shorting (excessive selling of the stock).
  - Until a buy-order is placed AND while we have a red candle, then the _trigger price_ associated with the _trigger candle_ is the highest value of a red candle
2. We find our first green candle.  (indicates beginning of potential up-turn)
3. The stock breaks the resistance identified by the _trigger price_ by at least $0.01.  (This can be modified by the user, but $0.01 over the resistance on a "well-behaved" stock is a decent indicator that a future up-turn is possible/within a respectable realm of probability)

### Selling

The sell-order criteria are still in the works, but might follow some combination of the below listed Methods:

***STOP-LOSS METHOD***
1. if the ticker drops below a certain price, then sell.  This is defined during the buy-order by some percentage of risk.  (i.e. if stock A is bought at $10 and you'd like to risk at most 20%, then the stop loss would be placed at $8).
2. The _STOP-LOSS_ price can be increased as the stock price increases.  (i.e. if stock A is bought at $10 and it increases to $12, the _STOP-LOSS_ can be increased to, say, $9 or $10 or $11.  Whatever the user decides.  Maybe the _STOP-LOSS_ increases by $0.50 for every $1.00 increase over the purchase price.  Or, maybe there is some sort of percentage rule: for every 10% increase in price, the _STOP-LOSS_ increases by 10%)

***REALIZE PROFITS METHOD***
1. Incorporate the _STOP-LOSS_ from above.
2. In addition, once the stock crosses a certain profit percentage threshold (defined by the user), sell!  This guarantees that once you've hit your desired percentage gain, you're out!  The intent is to limit "greediness."  However, with proper utilization of the _STOP-LOSS_ method, you could probably guarantee close to the same, and occasionally better, results.


## Disclaimers

### 1.
This code is currently incomplete and does not function as it should.  I've take a bit of a hiatus from this project for the time-being.  I'd say it's about 97.3% complete in regards to infrastructure, but the core trading-logic is at about 67.2%.

### 2.
The results of this program are not indicative of any financial prowess and should not be used as professional advice


## Absolution Clause
I, Quinton Wiebe, the creator of this program absolve myself of all responsibility in the case of lost funds.

In the case of increased funds, I take full responsibility
