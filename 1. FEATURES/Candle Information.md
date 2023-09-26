## Function Name
`candle_information`

## Description
The `candle_information` function takes a Pandas DataFrame containing Open, High, Low, and Close (OHLC) data as input and returns a new DataFrame with three additional columns: 'candle_way', 'filling', and 'amplitude'. These new columns provide insights into the nature of individual candlesticks in a financial chart.

## Parameters
- `df`: Pandas DataFrame containing the OHLC data.

## Returns
A new Pandas DataFrame containing three new columns:

- `candle_way`: Indicates the direction of the candle (-1 for bearish and 1 for bullish).
- `filling`: Ratio of the absolute difference between the close and open prices to the absolute difference between the high and low prices.
- `amplitude`: Measures the amplitude of the candle as a percentage, which is calculated based on the close and open prices.

## Python Code
```py
def candle_information(df):
    # Candle color
    df["candle_way"] = -1
    df.loc[(df["open"] - df["close"]) < 0, "candle_way"] = 1

    # Filling percentage
    df["filling"] = np.abs(df["close"] - df["open"]) / np.abs(df["high"] - df["low"])

    # Amplitude
    df["amplitude"] = np.abs(df["close"] - df["open"]) / (df["open"] / 2 + df["close"] / 2) * 100

    return df
```

## Usage Examples
To get candle information from an OHLC DataFrame named `ohlc_data`:



`new_data = candle_information(ohlc_data)`

## Notes

- This function is particularly useful for technical analysis in financial markets.
- 'candle_way' serves as a quick reference to understand the direction in which the market is moving.
- 'filling' and 'amplitude' can be used to measure the strength or volatility within a single trading period.

## Limitations

- Assumes that the DataFrame contains OHLC columns.
- NaN or missing values in the original DataFrame could affect the calculations.

## Additional Resources

- [Candlestick Charting - Wikipedia](https://en.wikipedia.org/wiki/Candlestick_chart)

## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)