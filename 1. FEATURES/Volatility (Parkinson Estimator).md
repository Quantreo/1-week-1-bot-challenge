
## Function Name
`moving_parkinson_estimator`

## Description
The `moving_parkinson_estimator` function calculates Parkinson's volatility estimator over a rolling window in a DataFrame containing high and low prices. Parkinson's estimator is a well-known method used to estimate the volatility of a financial instrument.

## Parameters
- `df`: Pandas DataFrame containing columns 'high' and 'low', which represent the high and low prices for each trading period.
- `window_size`: The size of the rolling window for which Parkinson's volatility is estimated. Default value is 30.

## Returns
A new Pandas DataFrame containing the original data plus a new column:

- `rolling_volatility_parkinson`: The estimated volatility based on Parkinson's method for each window.

## Python Code
```py
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
```


## Usage Examples

To calculate Parkinson's estimator in a DataFrame named `price_data` with a window size of 30:

`new_data = moving_parkinson_estimator(price_data, window_size=30)`

## Notes

- Useful for volatility estimation and for strategies that depend on an accurate measure of volatility.
- The larger the window size, the smoother the volatility curve will be, but it may lag behind in capturing sudden changes.

## Limitations

- Assumes that the DataFrame has 'high' and 'low' columns.
- Not applicable to data sets that don't contain these columns.
- The method assumes that the logarithmic price follows a Gaussian distribution, which may not always be the case in real-world financial data.

## Additional Resources
- [Volatility (finance) - Wikipedia](https://en.wikipedia.org/wiki/Volatility_(finance))

## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)