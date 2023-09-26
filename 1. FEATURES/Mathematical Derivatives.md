
## Function Name
`derivatives`

## Description
The `derivatives` function takes a Pandas DataFrame and a specified column as inputs and returns a new DataFrame with two new columns added: 'velocity' and 'acceleration'. These new columns contain the first and second derivatives of the DataFrame based on the specified column, respectively.

## Parameters
- `df`: Pandas DataFrame containing the data on which the derivation will be performed.
- `col`: Name of the column from which the derivatives will be calculated.

## Returns
A new Pandas DataFrame containing two new columns:

- `velocity`: The first derivative of the specified column.
- `acceleration`: The second derivative of the specified column.

## Python Code

```py
def derivatives(df,col):
    """
    Calculates the first and second derivatives of a given column in a DataFrame 
    and adds them as new columns 'velocity' and 'acceleration'.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the column for which derivatives are to be calculated.
        
    col : str
        The column name for which the first and second derivatives are to be calculated.

    Returns:
    --------
    df_copy : pandas.DataFrame
        A new DataFrame with 'velocity' and 'acceleration' columns added.

    """
    
    df_copy = df.copy()

    df_copy["velocity"] = df_copy[col].diff().fillna(0)
    df_copy["acceleration"] = df_copy["velocity"].diff().fillna(0)
    
    return df_copy
```

## Usage Examples
To calculate velocity and acceleration from the 'price' column in a DataFrame named `data`:

`new_data = derivatives(data, 'price')`

## Notes

- Missing values generated due to differentiation are filled with zeros.
- This function is particularly useful for analyzing financial time series, sensor data, etc.

## Limitations

- The DataFrame must contain at least two rows for the derivatives to be calculated.
- NaN values in the original column could affect the calculation of derivatives.

## Additional Resources

- [Numerical Differentiation - Wikipedia](https://en.wikipedia.org/wiki/Numerical_differentiation)

## Author
Lucas Inglese - [CEO of Quantreo](https://quantreo.com)
