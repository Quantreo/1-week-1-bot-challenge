
## Function Name
`moving_yang_zhang_estimator`

## Description
The `moving_yang_zhang_estimator` function calculates the Yang-Zhang volatility estimator over a rolling window in a DataFrame containing high, low, open, and close prices. The Yang-Zhang estimator is another method used for volatility estimation in financial markets that aims to improve the accuracy by combining both opening and closing prices.

## Parameters
- `df`: Pandas DataFrame containing columns 'high', 'low', 'open', and 'close', which represent the high, low, opening, and closing prices for each trading period.
- `window_size`: The size of the rolling window for which Yang-Zhang's volatility is estimated. Default value is 30.

## Returns
A new Pandas DataFrame containing the original data plus a new column:

- `rolling_volatility_yang_zhang`: The estimated volatility based on Yang-Zhang's method for each window.

## Python Code
```py
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
```


## Usage Examples

To calculate Yang-Zhang's estimator in a DataFrame named `price_data` with a window size of 30:
`new_data = moving_yang_zhang_estimator(price_data, window_size=30)`

## Notes
- Useful for more accurate volatility estimation, as it uses high, low, open, and close prices.
- Recommended for strategies that rely on precise volatility measurements.

## Limitations
- Assumes that the DataFrame has 'high', 'low', 'open', and 'close' columns.
- The method assumes that the logarithmic price changes follow a Gaussian distribution, which may not always hold in real-world financial data.

## Additional Resources
- [Volatility (finance) - Wikipedia](https://en.wikipedia.org/wiki/Volatility_(finance))

## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)