# dangerous_trades
## algorithms.smoothing module
### algorithms.smoothing.exponential_moving_average(data: List\[float], alpha: float = 0.6) → List\[float]

Computes and returns an estimate of the next value in a series.

An exponential moving average (EMA) is the weighted mean of “window” consecutive data points, where
more weight is given to recent data. The simple form of an EMA and the one used here is:
next_estimate = (alpha \* most_recent_data_point) + ((1-alpha) \* current_estimate)
#### Parameters:
- **data** (List\[float]): A list of numerical data points.
- **alpha** (float): The smoothing parameter alpha; 0 <= alpha <= 1
#### Returns:
- **List\[float]**: A list containing the moving averages.
### algorithms.smoothing.simple_moving_average(data: List\[float], window: int, approximate_start: bool = True) → List\[float]
A simple moving average (SMA) is the unweighted mean of “window” consecutive data points.
#### Parameters:
- **data** (List\[float\]): A list of numerical data points.
- **window** (int): The number of consecutive data points to average over.
- **approximate_start** (bool): If True, we approximate the averages of the first “window” elements.
### Returns:
- **List\[float\]**: A list containing the moving averages.
## strategies.backtesting module
### strategies.backtesting.exponential_moving_average(exchange, symbol: str, investment: float, alpha: float, timeframe: str = '1m', limit: int = 365) → float
Backtest the exponential moving average (SMA) strategy on historical data.
#### Parameters:
- **exchange** (ccxt.exchange): Exchange we wish to trade on.
- **symbol** (str): Asset that we want to backtest. EX: “BTC/USD”.
- **investment** (float): The amount of to start the simulation with.
- **alpha** (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
- **timeframe** (str): minutes (1m), days (1d), etc..
- **limit** (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)
#### Returns:
- **float**: Investment value after the simulation.
### strategies.backtesting.exponential_moving_average_crossover(exchange, symbol: str, investment: float, small_alpha: float, big_alpha: float, timeframe: str = '1d', limit: int = 365) → float
Backtest the exponential moving crossover strategy on historical data. This is more of a play thing than a true
strategy. But perhaps you find application for it.
#### Parameters:
- **exchange** (ccxt.exchange): Exchange we wish to trade on.
- **symbol** (str): Asset that we want to backtest. EX: “BTC/USD”.
- **investment** (float): Amount of money to begin simulation with
- **small_alpha** (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
- **big_alpha** (float): EMA parameter alpha 0 <= alpha <= 1, bigger number gives more weight to recent data.
- **timeframe** (str): minutes (1m), days (1d), etc..
- **limit** (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)
#### Returns:
- **float**: Investment value after the simulation.
### strategies.backtesting.hold(exchange, symbol: str, investment: float, timeframe: str, limit: int) → float
The most simple strategy and a good benchmark. Compute total return if you were to hold
an asset for a given duration.
#### Parameters:
- **exchange** (ccxt.exchange): Exchange we wish to trade on.
- **symbol** (str): Asset that we want to backtest. EX: “BTC/USD”.
- **investment** (float): The amount of to start the simulation with.
- **timeframe** (str): minutes (1m), days (1d), etc..
- **limit** (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)
#### Returns:
**float**: Investment value after simulation
### strategies.backtesting.moving_average_crossover(exchange, symbol: str, investment: float, short_window: int, long_window: int, timeframe: str = '1d', limit: int = 365) → float
Backtest the simple moving average (SMA) strategy on historical data.
#### Parameters:
- **exchange** (ccxt.exchange): Exchange we wish to trade on.
- **symbol** (str): Asset that we want to backtest. EX: “BTC/USD”.
- **investment** (float): Amount of money to begin simulation with
- **short_window** (int): Number of consecutive data points to compute average over.
- **long_window** (int): Number of consecutive data points to compute average over.
- **timeframe** (str): minutes (1m), days (1d), etc..
- **limit** (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)
#### Returns:
- **float**: Investment value after the simulation.
### strategies.backtesting.simple_moving_average(exchange, symbol: str, investment: float, window: int, timeframe: str = '1m', limit: int = 365) → float

Backtest the simple moving average (SMA) strategy on historical data.
#### Parameters:
- **exchange** (ccxt.exchange): Exchange we wish to trade on.
- **symbol** (str): Asset that we want to backtest. EX: “BTC/USD”.
- **investment** (float): The amount of to start the simulation with.
- **window** (int): Number of consecutive data points to compute average over.
- **timeframe** (str): minutes (1m), days (1d), etc..
- **limit** (int): number of datapoints in backtest. Some exchanges impose limits (300, 1000)
####  Returns:
- float: Investment value after the simulation.
## strategies.moving_averages module
### strategies.moving_averages.exponential_moving_average(exchange: Exchange, symbol: str, window: int, alpha: float, position: [Position](#strategies.moving_averages.Position)) → [Action](#strategies.moving_averages.Action)

Decides whether to buy, sell, or wait by analyzing an exponential moving average.
#### Parameters:
- **exchange** (ccxt.Exchange): The exchange we wish to trade on (ccxt)
- **symbol** (str): The symbol/ticker representing the asset to be traded
- **window** (int): The number of continuous values to consider prior to our prediction
- **alpha** (float): The smoothing parameter for our EMA, 0 <= alpha <= 1
- **position** (Position): Indicates whether the asset is currently being held
####  Returns:
- **Action**: The reccomended Action (buy, sell, or wait).
### strategies.moving_averages.exponential_moving_average_crossover(exchange: Exchange, symbol: str, small_alpha: float, big_alpha: float, position: [Position](#strategies.moving_averages.Position)) → [Action](#strategies.moving_averages.Action)
Decides whether to buy, sell, or wait given the users position and by analyzing an exponential moving average
crossover.
#### Parameters:
- **exchange** (ccxt.Exchange): The exchange we wish to trade on (ccxt)
- **symbol** (str): The symbol/ticker representing the asset to be traded
- **small_alpha** (float): The number of continuous values to consider for the shorter moving averages
- **big_alpha** (float): The number of continuous values to consider for the longer moving averages
- **position** (Position): Indicates whether the asset is currently being held
#### Returns:
- Action: The reccomended Action (buy, sell, or wait).
### strategies.moving_averages.moving_average_crossover(exchange: Exchange, symbol: str, short_window: int, long_window, position: [Position](#strategies.moving_averages.Position)) → [Action](#strategies.moving_averages.Action)

Decides whether to buy, sell, or wait given the users position and by analyzing a moving average crossover.
####  Parameters:
- **exchange** (ccxt.Exchange): The exchange we wish to trade on (ccxt)
- **symbol** (str): The symbol/ticker representing the asset to be traded
- **short_window** (int): The number of continuous values to consider for the shorter moving averages
- **long_window** (int): The number of continuous values to consider for the longer moving averages
- **position** (Position): Indicates whether the asset is currently being held
#### Returns:
- **Action**: The reccomended Action (buy, sell, or wait).
### strategies.moving_averages.simple_moving_average(exchange: Exchange, symbol: str, window: int, position: [Position](#strategies.moving_averages.Position)) → [Action](#strategies.moving_averages.Action)

Decides whether to buy, sell, or wait by analyzing a simple moving average.
#### Parameters:
- **exchange** (ccxt.Exchange): The exchange we wish to trade on (ccxt)
- **symbol** (str): The symbol/ticker representing the asset to be traded
- **window** (int): The number of continuous values to consider for the moving average
- **position** (Position): Indicates whether the asset is currently being held
#### Returns:
- **Action**: The reccomended Action (buy, sell, or wait).
