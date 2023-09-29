import numpy as np
import pandas as pd
import math
import ta
from statsmodels.tsa.stattools import adfuller


def derivatives(df,col):
    """
    Calculates the first and second derivatives of a given column in a DataFrame 
    and adds them as new columns 'velocity' and 'acceleration'.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the column for which derivatives are to be calculated.
        
    col : str
        The column name for which the first and second derivatives are to be calculated.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame with 'velocity' and 'acceleration' columns added.

    """
    
    df_copy = df.copy()

    df_copy["velocity"] = df_copy[col].diff().fillna(0)
    df_copy["acceleration"] = df_copy["velocity"].diff().fillna(0)
    
    return df_copy


def displacement_detection(df, type_range="standard", strengh=3, period=100):
    """
    This function calculates and adds a 'displacement' column to a provided DataFrame. Displacement is determined based on
    the 'candle_range' which is calculated differently according to the 'type_range' parameter. Then, it calculates the
    standard deviation of the 'candle_range' over a given period and sets a 'threshold'. If 'candle_range' exceeds this 'threshold',
    a displacement is detected and marked as 1 in the 'displacement' column.

    Parameters:
    df (pd.DataFrame): The DataFrame to add the columns to. This DataFrame should have 'open', 'close', 'high', and 'low' columns.
    type_range (str, optional): Defines how to calculate 'candle_range'. 'standard' calculates it as the absolute difference between
                                'close' and 'open', 'extremum' calculates it as the absolute difference between 'high' and 'low'.
                                Default is 'standard'.
    strengh (int, optional): The multiplier for the standard deviation to set the 'threshold'. Default is 3.
    period (int, optional): The period to use for calculating the standard deviation. Default is 100.

    Returns:
    pd.DataFrame: The original DataFrame, but with four new columns: 'candle_range', 'MSTD', 'threshold' and 'displacement'.

    Raises:
    ValueError: If an unsupported 'type_range' is provided.
    """
    df_copy = df.copy()

    # Choose your type_range
    if type_range == "standard":
        df_copy["candle_range"] = np.abs(df_copy["close"] - df_copy["open"])
    elif type_range == "extremum":
        df_copy["candle_range"] = np.abs(df_copy["high"] - df_copy["low"])
    else:
        raise ValueError("Put a right format of type range")

    # Compute the STD of the candle range
    df_copy["MSTD"] = df_copy["candle_range"].rolling(period).std()
    df_copy["threshold"] = df_copy["MSTD"] * strengh

    # Displacement if the candle range is above the threshold
    df_copy["displacement"] = np.nan
    df_copy.loc[df_copy["threshold"] < df_copy["candle_range"], "displacement"] = 1
    df_copy["variation"] = df_copy["close"] - df_copy["open"]

    # Specify the way of the displacement
    df_copy["green_displacement"] = 0
    df_copy["red_displacement"] = 0

    df_copy.loc[(df_copy["displacement"] == 1) & (0 < df_copy["variation"]), "green_displacement"] = 1
    df_copy.loc[(df_copy["displacement"] == 1) & (df_copy["variation"] < 0), "red_displacement"] = 1

    # Shift by one because we only know that we have a displacement at the end of the candle (BE CAREFUL)
    df_copy["green_displacement"] = df_copy["green_displacement"].shift(1)
    df_copy["red_displacement"] = df_copy["red_displacement"].shift(1)

    df_copy["high_displacement"] = np.nan
    df_copy["low_displacement"] = np.nan

    df_copy.loc[df_copy["displacement"] == 1, "high_displacement"] = df_copy["high"]
    df_copy.loc[df_copy["displacement"] == 1, "low_displacement"] = df_copy["low"]

    df_copy["high_displacement"] = df_copy["high_displacement"].fillna(method="ffill")
    df_copy["low_displacement"] = df_copy["low_displacement"].fillna(method="ffill")

    return df_copy

def gap_detection(df, lookback=2):
    """
    Detects and calculates the bullish and bearish gaps in the given DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame with columns 'high' and 'low' representing the high and low prices for each period.
    - lookback (int, optional): Number of periods to look back to detect gaps. Default is 2.

    Returns:
    - pd.DataFrame: DataFrame with additional columns:
        * 'Bullish_gap_sup': Upper boundary of the bullish gap.
        * 'Bullish_gap_inf': Lower boundary of the bullish gap.
        * 'Bearish_gap_sup': Upper boundary of the bearish gap.
        * 'Bearish_gap_inf': Lower boundary of the bearish gap.
        * 'Bullish_gap_size': Size of the bullish gap.
        * 'Bearish_gap_size': Size of the bearish gap.

    The function first identifies the bullish and bearish gaps by comparing the current period's high/low prices
    with the high/low prices of the lookback period. It then calculates the size of each gap and forward-fills any
    missing values in the gap boundaries.
    """
    df_copy = df.copy()
    df_copy["Bullish_gap_sup"] = np.nan
    df_copy["Bullish_gap_inf"] = np.nan

    df_copy["Bearish_gap_sup"] = np.nan
    df_copy["Bearish_gap_inf"] = np.nan

    df_copy["Bullish_gap"] = 0
    df_copy["Bearish_gap"] = 0

    df_copy.loc[df_copy["high"].shift(lookback) < df_copy["low"], "Bullish_gap_sup"] = df_copy["low"]
    df_copy.loc[df_copy["high"].shift(lookback) < df_copy["low"], "Bullish_gap_inf"] = df_copy["high"].shift(lookback)
    df_copy.loc[df_copy["high"].shift(lookback) < df_copy["low"], "Bullish_gap"] = 1

    df_copy.loc[df_copy["high"] < df_copy["low"].shift(lookback), "Bearish_gap_sup"] = df_copy["low"].shift(lookback)
    df_copy.loc[df_copy["high"] < df_copy["low"].shift(lookback), "Bearish_gap_inf"] = df_copy["high"]
    df_copy.loc[df_copy["high"] < df_copy["low"].shift(lookback), "Bearish_gap"] = 1

    df_copy["Bullish_gap_size"] = df_copy["Bullish_gap_sup"] - df_copy["Bullish_gap_inf"]
    df_copy["Bearish_gap_size"] = df_copy["Bearish_gap_sup"] - df_copy["Bearish_gap_inf"]

    # Fill the missing values by the last one
    df_copy[["Bullish_gap_sup", "Bullish_gap_inf",
        "Bearish_gap_sup", "Bearish_gap_inf"]] = df_copy[["Bullish_gap_sup", "Bullish_gap_inf",
                                                     "Bearish_gap_sup", "Bearish_gap_inf"]].fillna(method="ffill")

    return df_copy

def candle_information(df):
    # Candle color
    df["candle_way"] = -1
    df.loc[(df["open"] - df["close"]) < 0, "candle_way"] = 1

    # Filling percentage
    df["filling"] = np.abs(df["close"] - df["open"]) / np.abs(df["high"] - df["low"])

    # Amplitude
    df["amplitude"] = np.abs(df["close"] - df["open"]) / (df["open"] / 2 + df["close"] / 2) * 100

    return df


def moving_parkinson_estimator(df, window_size=30):
    """
    Calculate Parkinson's volatility estimator based on high and low prices.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing 'high' and 'low' columns for each trading period.

    Returns:
    --------
    volatility : float
        Estimated volatility based on Parkinson's method.
    """
    def parkinson_estimator(df):
        N = len(df)
        sum_squared = np.sum(np.log(df['high'] / df['low']) ** 2)

        volatility = math.sqrt((1 / (4 * N * math.log(2))) * sum_squared)
        return volatility
    
    df_copy = df.copy()
    # Create an empty series to store mobile volatility
    rolling_volatility = pd.Series(dtype='float64')

    # Browse the DataFrame by window size `window_size` and apply `parkinson_estimator`.
    for i in range(window_size, len(df)):
        window = df_copy.loc[df_copy.index[i-window_size]: df_copy.index[i]]
        volatility = parkinson_estimator(window)
        rolling_volatility.at[df_copy.index[i]] = volatility

    # Add the mobile volatility series to the original DataFrame
    df_copy['rolling_volatility_parkinson'] = rolling_volatility
    
    return df_copy

def moving_yang_zhang_estimator(df, window_size=30):
    """
    Calculate Parkinson's volatility estimator based on high and low prices.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing 'high' and 'low' columns for each trading period.

    Returns:
    --------
    volatility : float
        Estimated volatility based on Parkinson's method.
    """
    def yang_zhang_estimator(df):
        N = len(window)
    
        term1 = np.log(window['high'] / window['close']) * np.log(window['high'] / window['open'])
        term2 = np.log(window['low'] / window['close']) * np.log(window['low'] / window['open'])

        sum_squared = np.sum(term1 + term2)
        volatility = np.sqrt(sum_squared / N)

        return volatility
    
    df_copy = df.copy()
    
    # Create an empty series to store mobile volatility
    rolling_volatility = pd.Series(dtype='float64')

    # Browse the DataFrame by window size `window_size` and apply `yang_zhang_estimator`.
    for i in range(window_size, len(df)):
        window = df_copy.loc[df_copy.index[i-window_size]: df_copy.index[i]]
        volatility = yang_zhang_estimator(window)
        rolling_volatility.at[df_copy.index[i]] = volatility

    # Add the mobile volatility series to the original DataFrame
    df_copy['rolling_volatility_yang_zhang'] = rolling_volatility
    
    return df_copy


def kama(df, col, n):
    """
    Calculates the Kaufman Adaptive Moving Average (KAMA) for a specified column
    in a DataFrame and adds it as a new column named 'kama_{n}'.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the column for which KAMA is to be calculated.
    col : str
        The name of the column for which KAMA will be calculated.
    n : int
        The window period for KAMA calculation.
    
    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame with the 'kama_{n}' column added.
    """
    df_copy = df.copy()
    df_copy[f"kama_{n}"] = ta.momentum.KAMAIndicator(df_copy[col], n).kama()
    
    return df_copy


def DC_market_regime(df, threshold):
    """
    Determines the market regime based on Directional Change (DC) and trend events.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        A DataFrame containing financial data. The DataFrame should contain a 'close' column 
        with the closing prices, and 'high' and 'low' columns for high and low prices.
    
    threshold : float
        The percentage threshold for DC events.
    
    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame containing the original data and a new column "market_regime", 
        which indicates the market regime at each timestamp. A value of 1 indicates 
        an upward trend, and a value of 0 indicates a downward trend.
        
    """
    def dc_event(Pt, Pext, threshold):
        """
        Compute if we have a POTENTIAL DC event
        """
        var = (Pt - Pext) / Pext

        if threshold <= var:
            dc = 1
        elif var <= -threshold:
            dc = -1
        else:
            dc = 0

        return dc


    def calculate_dc(df, threshold):
        """
        Compute the start and the end of a DC event
        """

        # Initialize lists to store DC and OS events
        dc_events_up = []
        dc_events_down = []
        dc_events = []
        os_events = []

        # Initialize the first DC event
        last_dc_price = df["close"][0]
        last_dc_direction = 0  # +1 for up, -1 for down

        # Initialize the current Min & Max for the OS events
        min_price = last_dc_price
        max_price = last_dc_price
        idx_min = 0
        idx_max = 0


        # Iterate over the price list
        for i, current_price in enumerate(df["close"]):

            # Update min & max prices
            try:
                max_price = df["high"].iloc[dc_events[-1][-1]:i].max()
                min_price = df["low"].iloc[dc_events[-1][-1]:i].min()
                idx_min = df["high"].iloc[dc_events[-1][-1]:i].idxmin()
                idx_max = df["low"].iloc[dc_events[-1][-1]:i].idxmax()
            except Exception as e:
                pass
                #print(e, dc_events, i)
                #print("We are computing the first DC")

            # Calculate the price change in percentage
            dc_price_min = dc_event(current_price, min_price, threshold)
            dc_price_max = dc_event(current_price, max_price, threshold)


            # Add the DC event with the right index IF we are in the opposite way
            # Because if we are in the same way, we just increase the OS event size
            if (last_dc_direction!=1) & (dc_price_min==1):
                dc_events_up.append([idx_min, i])
                dc_events.append([idx_min, i])
                last_dc_direction = 1

            elif (last_dc_direction!=-1) & (dc_price_max==-1):
                dc_events_down.append([idx_max, i])
                dc_events.append([idx_max, i])
                last_dc_direction = -1

        return dc_events_up, dc_events_down, dc_events


    def calculate_trend(dc_events_down, dc_events_up, df):
        """
        Compute the DC + OS period (trend) using the DC event lists
        """

        # Initialize the variables
        trend_events_up = []
        trend_events_down = []

        # Verify which event occured first (upward or downward movement)

        # If the first event is a downward event
        if dc_events_down[0][0]==0:

            # Iterate on the index 
            for i in range(len(dc_events_down)):

                # If it is the value before the last one we break the loop
                if i==len(dc_events_down)-1:
                    break

                # Calculate the start and end for each trend
                trend_events_up.append([dc_events_up[i][1], dc_events_down[i+1][1]])
                trend_events_down.append([dc_events_down[i][1], dc_events_up[i][1]])

        # If the first event is a upward event
        elif dc_events_up[0][0]==0:

            # Iterate on the index
            for i in range(len(dc_events_up)):

                # If it is the value before the last one we break the loop
                if i==len(dc_events_up)-1:
                    break

                # Calculate the start and end for each trend
                trend_events_up.append([dc_events_down[i][1], dc_events_up[i+1][1]])
                trend_events_down.append([dc_events_up[i][1], dc_events_down[i][1]])

        # Verify the last indexed value for the down ward and the upward trends
        last_up = trend_events_up[-1][1]
        last_down = trend_events_down[-1][1]

        # Find which trend occured last to make it go until now
        if last_down < last_up:
            trend_events_up[-1][1] = len(df)-1
        else:
            trend_events_down[-1][1] = len(df)-1

        return trend_events_down, trend_events_up

    def get_dc_price(dc_events, df):
        dc_events_prices = []
        for event in dc_events:
            prices = [df["close"].iloc[event[0]], df["close"].iloc[event[1]]]
            dc_events_prices.append(prices)
        return dc_events_prices
    
    df_copy = df.copy()
    
    # Extract DC and Trend events
    dc_events_up, dc_events_down, dc_events = calculate_dc(df_copy, threshold=threshold)
    trend_events_down, trend_events_up = calculate_trend(dc_events_down, dc_events_up, df_copy)
    
    df_copy["market_regime"] = np.nan
    for event_up in trend_events_up:
        df_copy.loc[df_copy.index[event_up[1]], "market_regime"] = 1

    for event_down in trend_events_down:
        df_copy.loc[df_copy.index[event_down[1]], "market_regime"] = 0

    df_copy["market_regime"] = df_copy["market_regime"].fillna(method="ffill")
    
    return df_copy

def spread(df):
    """
    Calculates the spread between the 'high' and 'low' columns of a given DataFrame 
    and adds it as a new column named 'spread'.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the 'high' and 'low' columns for which the spread is to be calculated.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame with the 'spread' column added.
    """
    df_copy = df.copy()
    df_copy["spread"] = df_copy["high"] - df_copy["low"]
    
    return df_copy

def kama_market_regime(df, col, n, m):
    """
    Calculates the Kaufman's Adaptive Moving Average (KAMA) to determine market regime.
    
    Parameters:
    - df (pd.DataFrame): Input DataFrame containing price data or other numeric series.
    - col (str): The column name in the DataFrame to apply KAMA.
    - n (int): The period length for the first KAMA calculation.
    - m (int): The period length for the second KAMA calculation.

    Returns:
    - pd.DataFrame: DataFrame with additional columns "kama_diff" and "kama_trend" indicating the market trend.
    """
    
    df_copy = df.copy()
    df_copy = kama(df_copy, col, n)
    df_copy = kama(df_copy, col, m)

    df_copy["kama_diff"] = df_copy[f"kama_{m}"] - df_copy[f"kama_{n}"]
    df_copy["kama_trend"] = -1
    df_copy.loc[0<df_copy["kama_diff"], "kama_trend"] = 1
    
    return df_copy

def auto_corr(df, col, n=50, lag=10):
    """
    Calculates the autocorrelation for a given column in a Pandas DataFrame, using a specified window size and lag.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the column for which to compute autocorrelation.
    - col (str): The name of the column in the DataFrame for which to calculate autocorrelation.
    - n (int, optional): The size of the rolling window for calculation. Default is 50.
    - lag (int, optional): The lag step to be used when computing autocorrelation. Default is 10.

    Returns:
    - pd.DataFrame: A new DataFrame with an additional column named 'autocorr_{lag}', where {lag} is the provided lag value. This column contains the autocorrelation values.
    """
    df_copy = df.copy()
    df_copy[f'autocorr_{lag}'] = df_copy[col].rolling(window=n, min_periods=n, center=False).apply(lambda x: x.autocorr(lag=lag), raw=False)
    return df_copy

def log_transform(df, col, n):
    """
    Applies a logarithmic transformation to a specified column in a DataFrame 
    and calculates the percentage change of the log-transformed values over a 
    given window size.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the column to be logarithmically transformed.
    col : str
        The name of the column to which the logarithmic transformation is to be applied.
    n : int
        The window size over which to calculate the percentage change of the log-transformed values.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame containing two new columns:
        1. log_{col}: Log-transformed values of the specified column.
        2. ret_log_{n}: Percentage change of the log-transformed values over the window size n.
    """
    df_copy = df.copy()
    df_copy[f"log_{col}"] = np.log(df_copy[col])
    df_copy[f"ret_log_{n}"] = df_copy[f"log_{col}"].pct_change(n)
    
    return df_copy

def rolling_adf(df, col, window_size=30):
    """
    Calculate the Augmented Dickey-Fuller test statistic on a rolling window.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the column on which to perform the ADF test.
    col : str
        The name of the column on which to perform the ADF test.
    window_size : int
        The size of the rolling window.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame with an additional column containing the rolling ADF test statistic.
    """
    from statsmodels.tsa.stattools import adfuller

    df_copy = df.copy()
    
    # Create an empty series to store rolling ADF test statistic
    rolling_adf_stat = pd.Series(dtype='float64', index=df_copy.index)

    # Loop through the DataFrame by `window_size` and apply `adfuller`.
    for i in range(window_size, len(df)):
        window = df_copy[col].iloc[i-window_size:i]
        adf_result = adfuller(window)
        adf_stat = adf_result[0]
        rolling_adf_stat.at[df_copy.index[i]] = adf_stat

    # Add the rolling ADF test statistic series to the original DataFrame
    df_copy['rolling_adf_stat'] = rolling_adf_stat
    
    return df_copy