## Function Name
`gap_detection`

## Description
The `gap_detection` function detects and calculates bullish and bearish gaps in a given DataFrame containing high and low price data. Gaps represent significant price movements between periods and are an important aspect of technical analysis in trading.

## Parameters
- `df`: Pandas DataFrame containing columns 'high' and 'low', representing the high and low prices for each period.
- `lookback`: Integer (optional). Number of periods to look back for detecting gaps. Default is 2.

## Returns
A new Pandas DataFrame containing the original data and several new columns:

- `Bullish_gap_sup`: Upper boundary of the bullish gap.
- `Bullish_gap_inf`: Lower boundary of the bullish gap.
- `Bearish_gap_sup`: Upper boundary of the bearish gap.
- `Bearish_gap_inf`: Lower boundary of the bearish gap.
- `Bullish_gap_size`: Size of the bullish gap (Difference between 'Bullish_gap_sup' and 'Bullish_gap_inf').
- `Bearish_gap_size`: Size of the bearish gap (Difference between 'Bearish_gap_sup' and 'Bearish_gap_inf').
- `Bullish_gap`: Flag indicating the presence of a bullish gap (1 if true, 0 otherwise).
- `Bearish_gap`: Flag indicating the presence of a bearish gap (1 if true, 0 otherwise).

## Python Code
```py
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
```


## Usage Examples

To detect gaps in a DataFrame named `price_data` with a lookback of 2 periods:

pythonCopy code

`new_data = gap_detection(price_data, lookback=2)`

## Notes

- Useful for identifying potential turning points in price movements.
- Customize the detection by setting the `lookback` parameter to match your specific needs.

## Limitations

- Assumes that the DataFrame has 'high' and 'low' columns.
- Not applicable to non-OHLC data or data with missing values.
- Gaps are calculated based on a fixed lookback period and do not account for trading volume or other factors.

## Additional Resources
- [Market Gap - Investopedia](https://www.investopedia.com/terms/g/gap.asp)

## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)