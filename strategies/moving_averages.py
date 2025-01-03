from enum import Enum
from algorithms import smoothing

import ccxt

class Position(Enum):
    """Indicates whether we are currently holding the asset."""
    IN = "IN"
    OUT = "OUT"

class Action(Enum):
    """Indicates the reccomended action."""
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


def simple_moving_average(exchange: ccxt.Exchange, symbol: str, window: int, position: Position) -> Action:
    """
    Decides whether to buy, sell, or wait by analyzing a simple moving average.

    Parameters:
    - exchange(ccxt.Exchange): The exchange we wish to trade on (ccxt)
    - symbol (str): The symbol/ticker representing the asset to be traded
    - window (int): The number of continuous values to consider for the moving average 
    - position (Position): Indicates whether the asset is currently being held

    Returns:
    - Action: The reccomended Action (buy, sell, or wait).
    """
    
    # get asset prices for period of interest and compute moving averages
    ohlcv = exchange.fetch_ohlcv(symbol, "1d", limit=window+1)
    price_curve: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    averages: List[float] = smoothing.simple_moving_average(price_curve, window, approximate_start=True)
    
    # determine reccomended position given position and averages
    reccomended_position: Position = Position.IN if averages[0] < averages[1] else Position.OUT

    if(reccomended_position == position):
        return Action.WAIT
    elif(reccomended_position == Position.IN and position == Position.OUT):
        return Action.BUY
    else:
        return Action.SELL


def exponential_moving_average(exchange: ccxt.Exchange, symbol: str, window: int, alpha: float, position: Position) -> Action:
    """
    Decides whether to buy, sell, or wait by analyzing an exponential moving average.

    Parameters:
    - exchange(ccxt.Exchange): The exchange we wish to trade on (ccxt)
    - symbol (str): The symbol/ticker representing the asset to be traded
    - window (int): The number of continuous values to consider prior to our prediction
    - alpha (float): The smoothing parameter for our EMA, 0 <= alpha <= 1
    - position (Position): Indicates whether the asset is currently being held

    Returns:
    - Action: The reccomended Action (buy, sell, or wait).
    """
    
    if window < 2:
       raise ValueError("The Window parameter must be atleast two.")

    # get asset prices for period of interest and compute moving averages
    ohlcv = exchange.fetch_ohlcv(symbol, "1d", limit=window)
    price_curve: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    averages: List[float] = smoothing.exponential_moving_average(price_curve, alpha)
    
    # determine reccomended position given position and averages
    reccomended_position: Position = Position.IN if averages[-2] < averages[-1] else Position.OUT

    if(reccomended_position == position):
        return Action.WAIT
    elif(reccomended_position == Position.IN and position == Position.OUT):
        return Action.BUY
    else:
        return Action.SELL


def moving_average_crossover(exchange: ccxt.Exchange, symbol: str, short_window: int, long_window, position: Position) -> Action:
    """
    Decides whether to buy, sell, or wait given the users position and by analyzing a moving average crossover.

    Parameters:
    - exchange(ccxt.Exchange): The exchange we wish to trade on (ccxt)
    - symbol (str): The symbol/ticker representing the asset to be traded
    - short_window (int): The number of continuous values to consider for the shorter moving averages
    - long_window (int): The number of continuous values to consider for the longer moving averages
    - position (Position): Indicates whether the asset is currently being held

    Returns:
    - Action: The reccomended Action (buy, sell, or wait).
    """
    
    # get asset prices for period of interest and compute moving averages
    ohlcv = exchange.fetch_ohlcv(symbol, "1d", limit=long_window)
    price_curve: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    short_averages: List[float] = smoothing.simple_moving_average(price_curve, short_window, approximate_start=False)
    long_averages: List[float] = smoothing.simple_moving_average(price_curve, long_window, approximate_start=False)
    
    # determine reccomended position given position and averages
    reccomended_position: Position = Position.IN if long_averages[-1] < short_averages[-1] else Position.OUT

    if(reccomended_position == position):
        return Action.WAIT
    elif(reccomended_position == Position.IN and position == Position.OUT):
        return Action.BUY
    else:
        return Action.SELL


def exponential_moving_average_crossover(exchange: ccxt.Exchange, symbol: str, small_alpha: float, big_alpha: float,
                                         position: Position) -> Action:
    """
    Decides whether to buy, sell, or wait given the users position and by analyzing an exponential moving average 
    crossover.

    Parameters:
    - exchange(ccxt.Exchange): The exchange we wish to trade on (ccxt)
    - symbol (str): The symbol/ticker representing the asset to be traded
    - small_alpha (float): The number of continuous values to consider for the shorter moving averages
    - big_alpha (float): The number of continuous values to consider for the longer moving averages
    - position (Position): Indicates whether the asset is currently being held

    Returns:
    - Action: The reccomended Action (buy, sell, or wait).
    """
    
    # get asset prices for period of interest and compute moving averages
    ohlcv = exchange.fetch_ohlcv(symbol, "1d", limit=365)
    price_curve: List[float] = [ohlcv[i][4] for i in range(len(ohlcv))]
    long_averages: List[float] = smoothing.exponential_moving_average(price_curve, small_alpha)  # less reactive
    short_averages: List[float] = smoothing.exponential_moving_average(price_curve, big_alpha)  # more reactive
    
    # determine reccomended position given position and averages
    reccomended_position: Position = Position.IN if long_averages[-1] < short_averages[-1] else Position.OUT

    if(reccomended_position == position):
        return Action.WAIT
    elif(reccomended_position == Position.IN and position == Position.OUT):
        return Action.BUY
    else:
        return Action.SELL
