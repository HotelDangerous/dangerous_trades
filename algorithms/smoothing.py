from typing import List

def simple_moving_average(data: List[float], window: int, approximate_start: bool=True) -> List[float]:
    """
    Computes and returns the simple moving average (SMA) over a list of numbers.

    A simple moving average (SMA) is the unweighted mean of "window" consecutive data points.

    Parameters:
    - data (List[float]): A list of numerical data points.
    - window (int): The number of consecutive data points to average over.
    - approximate_start (bool): If True, we approximate the averages of the first "window" elements.

    Returns:
    - List[float]: A list containing the moving averages.
    """
    
    # check if window size is valid
    if window <= 0:
        raise ValueError("window must be a positive integer.")
    if window > len(data):
        raise ValueError("window cannot be larger than the dataset")

    # define variables necessary for computation
    sma: List[float] = []
    average: float = 0

    # if requested, approximate a smooth average for the first "window" values
    if (approximate_start):
        sma.append(data[0])
        for i in range(1, window):
            average = sum(data[0:i])/i
            sma.append(average)

        # compute moving average for the rest of the values
        for i in range(window, len(data)):
            average += (data[i] - data[i-window])/window
            sma.append(average)
    else:
        # compute the first moving average 
        average = sum(data[0:window])/window
        sma.append(average)

        for i in range(1, len(data)):
            average += (data[i] - data[i-window])/window
            sma.append(average)

    return sma


def exponential_moving_average(data: List[float], alpha: float=0.6) -> List[float]:
    """
    Computes and returns an estimate of the next value in a series.

    An exponential moving average (EMA) is the weighted mean of "window" consecutive data points, where 
    more weight is given to recent data. The simple form of an EMA and the one used here is:
    next_estimate = (alpha * most_recent_data_point) + ((1-alpha) * current_estimate)

    Parameters:
    - data (List[float]): A list of numerical data points.
    - alpha (float): The smoothing parameter alpha; 0 <= alpha <= 1

    Returns:
    - List[float]: A list containing the moving averages.
    """

    # define variables necessary for computation
    smoothed_curve: List[float] = [data[0]]
    current_estimate: float = data[0]  # initial condition

    # compute the exponential moving average for the rest of the time-series
    for i in range(1, len(data)):
        current_estimate = (alpha*data[i]) + ((1-alpha) * current_estimate)
        smoothed_curve.append(current_estimate)
    
    return smoothed_curve
