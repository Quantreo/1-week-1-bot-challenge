
## Function Name
`kama_market_regime`

## Description
The `kama_market_regime` function calculates the Kaufman's Adaptive Moving Average (KAMA) for a specified column in a given DataFrame and uses it to determine the market regime. Market regimes are crucial for understanding the current market direction and can aid in investment and trading decisions.

## Parameters
- `df`: Pandas DataFrame containing price data or other numeric series.
- `col`: String. The column name in the DataFrame to apply KAMA.
- `n`: Integer. The period length for the first KAMA calculation.
- `m`: Integer. The period length for the second KAMA calculation.

## Returns
A new Pandas DataFrame containing the original data and two new columns:

- `kama_diff`: Difference between the two KAMA values calculated with periods `n` and `m`.
- `kama_trend`: Indicates the market regime. A value of 1 indicates an upward trend, and a value of -1 indicates a downward or neutral trend.

## Python Code

```py
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
    df_copy.loc[0<df["kama_diff"], "kama_trend"] = 1
    
    return df_copy
```

## Usage Examples

To determine the market regime in a DataFrame named `price_data` using KAMA for the 'close' column with periods of 10 and 30:

`new_data = kama_market_regime(price_data, 'close', 10, 30)`

## Notes

- Useful for trend-following strategies.
- `n` and `m` can be adjusted to better fit the asset's price characteristics.

## Limitations

- Assumes that the DataFrame has the specified column (`col`) for KAMA calculation.
- KAMA assumes a single directional trend; it may not perform well in sideways markets.

## Additional Resources

- [Kaufman's Adaptive Moving Average - Investopedia](https://www.investopedia.com/terms/k/kaufmans-adaptive-moving-average.asp)

## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)