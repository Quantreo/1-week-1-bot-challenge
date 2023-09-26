## Function Name
`kama`

## Description
The `kama` function calculates the Kaufman Adaptive Moving Average (KAMA) for a given column in a DataFrame using the `ta` library's `KAMAIndicator`. KAMA is a moving average that adjusts its length based on market volatility, making it more responsive in trending periods and less so in sideways markets.

## Parameters
- `df`: Pandas DataFrame containing the column for which KAMA is to be calculated.
- `col`: The name of the column for which KAMA will be calculated, usually "close" for closing prices.
- `n`: The window period for KAMA calculation, usually a positive integer.

## Returns
A new Pandas DataFrame containing the original data plus a new column:

- `kama_{n}`: The calculated KAMA values over the window period `n`.

## Python Code

```py
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
```




## Usage Examples

To calculate the KAMA for a DataFrame named `price_data` with a window period of 10:

`new_data = kama(price_data, "close", 10)`

## Notes

- Useful for trend-following and volatility-based strategies.
- Requires the `ta` library for technical analysis.

## Limitations

- Assumes that the DataFrame has the specified column for which KAMA will be calculated.
- Requires installation of the `ta` library.

## Additional Resources

- [Technical Analysis Library in Python (TA-Lib & ta)](https://technicalvgl.wordpress.com/2020/02/04/technical-analysis-library-in-python-ta-lib-ta/)

## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)