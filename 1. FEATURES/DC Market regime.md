## Function Name
`DC_market_trend`

## Description
The `DC_market_trend` function determines the market regime based on Directional Change (DC) and trend events in a given DataFrame containing high, low, and close price data. The market regime is an important aspect of technical analysis in trading, helping traders understand the current trend of the market.

## Parameters
- `df`: Pandas DataFrame containing columns 'high', 'low', and 'close', representing the high, low, and closing prices for each period.
- `threshold`: Float. The percentage threshold for DC events to be considered significant.

## Returns
A new Pandas DataFrame containing the original data and a new column:

- `market_regime`: Indicates the market regime at each timestamp. A value of 1 indicates an upward trend, and a value of 0 indicates a downward trend. The values are forward-filled until the next significant event.

## Python Code
```py
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
    df_copy = df.copy()
    
    # Extract DC and Trend events
    dc_events_up, dc_events_down, dc_events = calculate_dc(df_copy, threshold=threshold)
    trend_events_down, trend_events_up = calculate_trend(dc_events_down, dc_events_up, df_copy)
    
    df_copy["market_regime"] = np.nan
    for event_up in trend_events_up:
        df_copy.loc[event_up[1], "market_regime"] = 1

    for event_down in trend_events_down:
        df_copy.loc[event_down[1], "market_regime"] = 0

    df_copy["market_regime"] = df_copy["market_regime"].fillna(method="ffill")
    
    return df_copy
```

## Usage Examples

To determine the market regime in a DataFrame named `price_data` with a DC threshold of 0.02:
`new_data = DC_market_regime(price_data, threshold=0.02)`

## Notes
- Useful for identifying the general direction of the market.
- Customizable by setting the `threshold` parameter to match your specific needs.

## Limitations
- Assumes that the DataFrame has the required 'high', 'low', and 'close' columns.
- Not applicable to non-OHLC data or data with missing values.

## Additional Resources


## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)