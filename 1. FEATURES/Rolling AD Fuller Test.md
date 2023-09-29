## Function Name
`rolling_adf`

## Description
The `rolling_adf` function calculates the Augmented Dickey-Fuller (ADF) test statistic for a given column in a DataFrame over a rolling window. The ADF test is used to determine the presence of unit root in the series, helping to understand if the series is stationary or not.

## Parameters
- `df`: Pandas DataFrame containing the column for which the ADF test is to be calculated.
- `col`: The name of the column for which the ADF test will be applied, usually "close" for closing prices.
- `window_size`: The size of the rolling window over which the ADF test will be calculated.

## Returns
A new Pandas DataFrame containing the original data plus a new column:

- `adf_stat_{window_size}`: The calculated ADF statistics over the rolling window of size `window_size`.

## Python Code

```py
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
```


## Usage Examples

To calculate the rolling ADF statistic for a DataFrame named `price_data` with a window size of 30:
`new_data = rolling_adf(price_data, "close", 30)`

## Notes

- Useful for identifying market regimes and preparing data for time-series models.
- May require the `statsmodels` library for statistical models.

## Limitations

- Assumes that the DataFrame has the specified column for which the ADF test will be calculated.
- Requires installation of the `statsmodels` library.

## Additional Resources

- [Statsmodels Documentation](https://www.statsmodels.org/stable/index.html)

## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)