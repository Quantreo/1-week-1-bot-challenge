## Function Name

`displacement_detection`

## Description
The `displacement_detection` function calculates and adds a 'displacement' column, along with several other columns, to a given DataFrame with OHLC data (Open, High, Low, Close). The function allows for the detection of significant market movements or "displacements" based on a set 'threshold'.

## Parameters
- `df`: Pandas DataFrame containing OHLC data.
- `type_range`: String (optional). Defines how to calculate 'candle_range'. Can be 'standard' (calculates it as the absolute difference between 'close' and 'open') or 'extremum' (calculates it as the absolute difference between 'high' and 'low'). Default is 'standard'.
- `strengh`: Integer (optional). The multiplier for the standard deviation used to set the 'threshold'. Default is 3.
- `period`: Integer (optional). The period to use for calculating the standard deviation. Default is 100.

## Returns
A new Pandas DataFrame containing the original OHLC data and several new columns:

- `candle_range`: Calculated based on the `type_range` parameter.
- `MSTD`: Rolling standard deviation of the 'candle_range'.
- `threshold`: Calculated as `MSTD` times `strengh`.
- `displacement`: Indicates if a significant market movement has occurred (1 if true, NaN otherwise).
- `variation`: Close price minus open price.
- `green_displacement`: Indicates a bullish displacement (1 if true, 0 otherwise).
- `red_displacement`: Indicates a bearish displacement (1 if true, 0 otherwise).
- `high_displacement`: The high price at the time of displacement.
- `low_displacement`: The low price at the time of displacement.

## Python Code
```py
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
```

## Usage Examples

To detect displacement in an OHLC DataFrame named `ohlc_data`:
`new_data = displacement_detection(ohlc_data, type_range="standard", strengh=3, period=100)`

## Notes
- This function is useful for detecting significant price movements, which can be helpful for trading strategies.
- You can customize the detection method by tweaking the `type_range`, `strengh`, and `period` parameters.

## Limitations
- Assumes the DataFrame contains OHLC columns.
- `NaN` or missing values in the original DataFrame may affect the calculations.
- Caution: Displacement detection is shifted by one row. Be careful when using this feature for trading decisions.

## Additional Resources

- [Market Volatility - Wikipedia](https://en.wikipedia.org/wiki/Volatility_(finance))

## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)