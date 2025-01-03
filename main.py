import strategies.moving_averages as ma 
import strategies.backtesting as bt

from strategies.moving_averages import Position

import matplotlib.pyplot as plt
import ccxt

# constants
EXCHANGE = ccxt.coinbase()
SYMBOL = "BTC/USD"
INVESTMENT = 100000
SHORT_WINDOW = 3
LONG_WINDOW = 21
TIMEFRAME = "1d"
LIMIT = 90

# are we holding the asset (IN) or not (OUT)
BTC_POSITION = Position.OUT
DOGE_POSITION = Position.OUT
SHIB_POSITION = Position.OUT
BONK_POSITION = Position.OUT


# backtesting
total_return =bt.moving_average_crossover(EXCHANGE, SYMBOL, INVESTMENT, SHORT_WINDOW, LONG_WINDOW, TIMEFRAME, LIMIT)
print(f"Results: {INVESTMENT} -> {round(total_return, 2)}")


# buy, sell, wait reccomendation
print(f"BTC:  {ma.moving_average_crossover(EXCHANGE, "BTC/USD", SHORT_WINDOW, LONG_WINDOW, BTC_POSITION)}")
print(f"DOGE: {ma.moving_average_crossover(EXCHANGE, "DOGE/USD", SHORT_WINDOW, LONG_WINDOW, DOGE_POSITION)}")
print(f"SHIB: {ma.moving_average_crossover(EXCHANGE, "SHIB/USD", SHORT_WINDOW, LONG_WINDOW, SHIB_POSITION)}")
print(f"BONK: {ma.moving_average_crossover(EXCHANGE, "BONK/USD", SHORT_WINDOW, LONG_WINDOW, BONK_POSITION)}")

