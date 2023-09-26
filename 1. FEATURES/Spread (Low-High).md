
## Function Name
`spread`

## Description
The `spread` function calculates the spread between the 'high' and 'low' columns in a given DataFrame. The spread is simply the difference between the high and low prices of a security for a given period and is a measure of volatility.

## Parameters
- `df`: Pandas DataFrame containing columns 'high' and 'low', which represent the high and low prices for each period.

## Returns
A new Pandas DataFrame containing the original data plus a new column:

- `spread`: The calculated spread between the 'high' and 'low' columns.

## Python Code
```py
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
```


## Usage Examples

To calculate the spread in a DataFrame named `price_data`:

`new_data = spread(price_data)`

## Notes

- Useful for volatility analysis and trading strategies that capitalize on price volatility.

## Limitations

- Assumes that the DataFrame has 'high' and 'low' columns.
- Not applicable to data sets that don't contain these columns.

## Additional Resources


## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)