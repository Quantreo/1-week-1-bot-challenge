
## Function Name
`log_transform`

## Description
The `log_transform` function applies a logarithmic transformation to a specified column in a Pandas DataFrame and calculates the percentage change of the transformed values over a given window size `n`. Logarithmic transformations are often used to linearize exponential data or to work with returns in financial time series.

## Parameters
- `df`: Pandas DataFrame containing the column for which the logarithmic transformation and return will be calculated.
- `col`: String representing the name of the column in the DataFrame to which the logarithmic transformation is to be applied.
- `n`: Integer. The window size over which to calculate the percentage change of the log-transformed values.

## Returns
A new Pandas DataFrame containing the original data plus two new columns:

- `log_{col}`: Logarithmically transformed values of the specified `col`.
- `ret_log_{n}`: The percentage change of the logarithmically transformed values over the window size `n`.

## Python Code
```py
def log_transform(df, col, n):
    """
    Applies a logarithmic transformation to a specified column in a DataFrame 
    and calculates the percentage change of the log-transformed values over a 
    given window size.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the column to be logarithmically transformed.
    col : str
        The name of the column to which the logarithmic transformation is to be applied.
    n : int
        The window size over which to calculate the percentage change of the log-transformed values.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame containing two new columns:
        1. log_{col}: Log-transformed values of the specified column.
        2. ret_log_{n}: Percentage change of the log-transformed values over the window size n.
    """
    df_copy = df.copy()
    df_copy[f"log_{col}"] = np.log(df_copy[col])
    df_copy[f"ret_log_{n}"] = df_copy[f"log_{col}"].pct_change(n)
    
    return df_copy
```


## Usage Examples

To apply a logarithmic transformation and calculate the percentage change for a column named `close` in a DataFrame named `price_data` over a window size of 5:

`new_data = log_transform(price_data, col='close', n=5)`

## Notes
- Useful for converting exponential growth patterns to linear form.
- Helpful in financial time series analysis where log returns are often used.

## Limitations
- Assumes that the DataFrame contains the column specified in `col`.
- Assumes that all the values in the specified column are non-negative.
- Not applicable to data sets with zero or negative values in the specified column.

## Additional Resources


## Author

Lucas Inglese - [CEO of Quantreo](https://quantreo.com/)