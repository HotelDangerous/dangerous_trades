from typing import Callable, List
from strategies.moving_averages import Position

import algorithms.smoothing as smoothing
import matplotlib.pyplot as plt


def simple_moving_average(exchange, symbol: str, investment: float, window:int,
                                   timeframe: str="1m", limit: int=365) -> float:
    """
    Backtest the simple moving average (SMA) strategy on historical data.

    Parameters:
    - exchange (ccxt.exchange): Exchange we wish to trade on.
    - symbol (str): Asset that we want to backtest. EX: "BTC/USD".
    - investment (float): The amount of to start the simulation with.
    - window (int): Number of consecutive data points to compute average over.
    - timeframe (str): minutes (1m), days (1d), etc..
    - limit (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)

    Returns:
    - float: Investment value after the simulation.
    """
    
    # define variables
    position: Position = Position.OUT
    buy_price: float = 0
    sell_price: float = 0
    buys: List[List[int], List[float]] = [[], []]
    sells: List[List[int], List[float]] = [[], []]

    # get historical pricing data and compute smooth curve using SMA
    ohlcv: List[List] = exchange.fetch_ohlcv(symbol, timeframe, limit)
    historical_data: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    smoothed_data: List[float] = simple_moving_average(historical_data, window)
    
    # test trading strategy
    for i in range(1, len(smoothed_data)):
        if(smoothed_data[i-1] < smoothed_data[i]) and position == Position.OUT:
            # we want to buy 
            buy_price = historical_data[i]
            position = Position.IN
            investment *= 0.999  # simulate fees

            # log buy
            buys[0].append(i)
            buys[1].append(buy_price)
        
        if(smoothed_data[i-1] > smoothed_data[i]) and position == Position.IN:
            # we want to sell
            sell_price = historical_data[i]
            position = Position.OUT
            investment = investment * (sell_price / buy_price)
            investment *= 0.999  # simulate fees

            # log sell 
            sells[0].append(i)
            sells[1].append(sell_price)
    
    # plot lines
    plt.plot(historical_data, color="black")
    plt.plot(smoothed_data, color="red")

    #plot buy and sell points 
    plt.scatter(buys[0], buys[1], color="green")
    plt.scatter(sells[0], sells[1], color="red")

    plt.show()

    if position==Position.IN:
        investment = (investment * (historical_data[-1] / buy_price)) * .999

    return investment


def exponential_moving_average(exchange, symbol: str, investment: float, alpha: float, timeframe: str="1m",
                          limit: int=365) -> float:
    """
    Backtest the exponential moving average (SMA) strategy on historical data.

    Parameters:
    - exchange (ccxt.exchange): Exchange we wish to trade on.
    - symbol (str): Asset that we want to backtest. EX: "BTC/USD".
    - investment (float): The amount of to start the simulation with.
    - alpha (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
    - timeframe (str): minutes (1m), days (1d), etc..
    - limit (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)

    Returns:
    - float: Investment value after the simulation.
    """
    
    # define variables
    position: Position = Position.OUT
    buy_price: float = 0
    sell_price: float = 0
    buys: List[List[int], List[float]] = [[], []]
    sells: List[List[int], List[float]] = [[], []]

    # get historical pricing data and compute smooth curve using SMA
    ohlcv: List[List] = exchange.fetch_ohlcv(symbol, timeframe, limit)
    historical_data: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    smoothed_data: List[float] = smoothing.exponential_moving_average(historical_data, alpha)
    
    # test trading strategy
    for i in range(1, len(smoothed_data)):
        if(smoothed_data[i-1] < smoothed_data[i]) and position == Position.OUT:
            # we want to buy 
            buy_price = historical_data[i]
            position = Position.IN
            investment *= 0.999  # simulate fees

            # log buy
            buys[0].append(i)
            buys[1].append(buy_price)
        
        if(smoothed_data[i-1] > smoothed_data[i]) and position == Position.IN:
            # we want to sell
            sell_price = historical_data[i]
            position = Position.OUT
            investment = investment * (sell_price / buy_price)
            investment *= 0.999  # simulate fees

            # log sell 
            sells[0].append(i)
            sells[1].append(sell_price)
    
    # plot lines
    plt.plot(historical_data, color="black")
    plt.plot(smoothed_data, color="red")

    #plot buy and sell points 
    plt.scatter(buys[0], buys[1], color="green")
    plt.scatter(sells[0], sells[1], color="red")

    plt.show()

    if position==Position.IN:
        investment = (investment * (historical_data[-1] / buy_price)) * .999

    return investment
 

def moving_average_crossover(exchange, symbol: str, investment: float, short_window:int, long_window:int,
                             timeframe: str="1d", limit: int=365) -> float:
    """
    Backtest the simple moving average (SMA) strategy on historical data.

    Parameters:
    - exchange (ccxt.exchange): Exchange we wish to trade on.
    - symbol (str): Asset that we want to backtest. EX: "BTC/USD".
    - investment (float): Amount of money to begin simulation with
    - short_window (int): Number of consecutive data points to compute average over.
    - long_window (int): Number of consecutive data points to compute average over.
    - timeframe (str): minutes (1m), days (1d), etc..
    - limit (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)

    Returns:
    - float: Investment value after the simulation.
    """
    
    # define variables
    position: Position = Position.OUT
    recommended_position = Position.OUT
    buy_price: float = 0
    sell_price: float = 0
    buys: List[List[int], List[float]] = [[], []]
    sells: List[List[int], List[float]] = [[], []]

    # get historical pricing data and compute smooth curve using SMA
    ohlcv: List[List] = exchange.fetch_ohlcv(symbol, timeframe, limit)
    historical_data: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    short_average_data: List[float] = smoothing.simple_moving_average(historical_data, short_window)
    long_average_data: List[float] = smoothing.simple_moving_average(historical_data, long_window)

    
    # test trading strategy
    for i in range(1, len(historical_data)):

        recommended_position = Position.IN if long_average_data[i] < short_average_data[i] else Position.OUT

        if position == Position.OUT and recommended_position == Position.IN:
            # we want to buy 
            buy_price = historical_data[i]
            position = Position.IN
            investment *= 0.999  # simulate fees
            buys[0].append(i)
            buys[1].append(buy_price)
        
        if position == Position.IN and recommended_position == Position.OUT:
            # we want to sell
            sell_price = historical_data[i]
            position = Position.OUT
            investment = investment * (sell_price / buy_price)
            investment *= 0.999  # simulate fees
            sells[0].append(i)
            sells[1].append(sell_price)
    
    
    # plot lines
    plt.plot(historical_data, color="black")
    plt.plot(short_average_data, color="red")
    plt.plot(long_average_data, color="blue")

    #plot buy and sell points 
    plt.scatter(buys[0], buys[1], color="green")
    plt.scatter(sells[0], sells[1], color="red")

    plt.show()

    if position==Position.IN:
        investment = (investment * (historical_data[-1] / buy_price)) * .999

    return investment  


def exponential_moving_average_crossover(exchange, symbol: str, investment: float, small_alpha: float, big_alpha: float,
                             timeframe: str="1d", limit: int=365) -> float:
    """
    Backtest the exponential moving crossover strategy on historical data. This is more of a play thing than a true 
    strategy. But perhaps you find application for it.

    Parameters:
    - exchange (ccxt.exchange): Exchange we wish to trade on.
    - symbol (str): Asset that we want to backtest. EX: "BTC/USD".
    - investment (float): Amount of money to begin simulation with
    - small_alpha (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
    - big_alpha (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
    - timeframe (str): minutes (1m), days (1d), etc..
    - limit (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)

    Returns:
    - float: Investment value after the simulation.
    """
    
    # define variables
    position: Position = Position.OUT
    recommended_position = Position.OUT
    buy_price: float = 0
    sell_price: float = 0
    buys: List[List[int], List[float]] = [[], []]
    sells: List[List[int], List[float]] = [[], []]

    # get historical pricing data and compute smooth curve using SMA
    ohlcv: List[List] = exchange.fetch_ohlcv(symbol, timeframe, limit)
    historical_data: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    short_average_data: List[float] = smoothing.exponential_moving_average(historical_data, big_alpha)
    long_average_data: List[float] = smoothing.exponential_moving_average(historical_data, small_alpha)

    
    # test trading strategy
    for i in range(1, len(historical_data)):

        recommended_position = Position.IN if long_average_data[i] < short_average_data[i] else Position.OUT

        if position == Position.OUT and recommended_position == Position.IN:
            # we want to buy 
            buy_price = historical_data[i]
            position = Position.IN
            investment *= 0.999  # simulate fees
            buys[0].append(i)
            buys[1].append(buy_price)
        
        if position == Position.IN and recommended_position == Position.OUT:
            # we want to sell
            sell_price = historical_data[i]
            position = Position.OUT
            investment = investment * (sell_price / buy_price)
            investment *= 0.999  # simulate fees
            sells[0].append(i)
            sells[1].append(sell_price)
    
    
    # plot lines
    plt.plot(historical_data, color="black")
    plt.plot(short_average_data, color="red")
    plt.plot(long_average_data, color="blue")

    #plot buy and sell points 
    plt.scatter(buys[0], buys[1], color="green")
    plt.scatter(sells[0], sells[1], color="red")

    plt.show()

    if position==Position.IN:
        investment = (investment * (historical_data[-1] / buy_price)) * .999

    return investment

 
