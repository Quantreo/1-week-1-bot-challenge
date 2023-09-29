import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta


def get_barrier_buy(df, nb_row, tp=0.015, sl=-0.015):
    i = nb_row
    # LOOP FOR UNTIL WE CROSS THE TP OR SL
    for j in range(5000):

        # Extract starting line
        row_i = df.iloc[i:i + 1]

        # Extract current line
        row_i_j = df.iloc[i + j:i + j + 1]

        # Compute variations from the start to current high and low
        var_high = (row_i_j["high"].values[0] - row_i["open"].values[0]) / row_i["open"].values[0]
        var_low = (row_i_j["low"].values[0] - row_i["open"].values[0]) / row_i["open"].values[0]

        if (tp < var_high) and (var_low < sl):
            if row_i_j["high_time"].values[0] < row_i_j["low_time"].values[0]:
                time_datetime = datetime.strptime(row_i_j["high_time"].values[0],
                                                  "%Y-%m-%d %H:%M:%S") - datetime.strptime(row_i["time"].values[0],
                                                                                           "%Y-%m-%d %H:%M:%S")
                break
            elif row_i_j["low_time"].values[0] < row_i_j["high_time"].values[0]:
                time_datetime = -(datetime.strptime(row_i_j["low_time"].values[0],
                                                    "%Y-%m-%d %H:%M:%S") - datetime.strptime(
                    row_i["time"].values[0], "%Y-%m-%d %H:%M:%S"))
                break

        # IF we touch the tp we break the loop
        elif (tp < var_high):
            time_datetime = datetime.strptime(row_i_j["high_time"].values[0],
                                              "%Y-%m-%d %H:%M:%S") - datetime.strptime(row_i["time"].values[0],
                                                                                       "%Y-%m-%d %H:%M:%S")
            break

        # IF we touch the sl we break the loop
        elif (var_low < sl):
            time_datetime = -(
                        datetime.strptime(row_i_j["low_time"].values[0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(
                    row_i["time"].values[0], "%Y-%m-%d %H:%M:%S"))
            break

        else:
            time_datetime = timedelta(0)

    time = time_datetime.total_seconds() / 3600
    return time
def get_barrier_sell(df, nb_row, tp=0.015, sl=-0.015):
    i = nb_row
    # LOOP FOR UNTIL WE CROSS THE TP OR SL
    for j in range(5000):

        # Extract starting line
        row_i = df.iloc[i:i + 1]

        # Extract current line
        row_i_j = df.iloc[i + j:i + j + 1]

        # Compute variations from the start to current high and low
        var_high = (row_i_j["high"].values[0] - row_i["open"].values[0]) / row_i["open"].values[0]
        var_low = (row_i_j["low"].values[0] - row_i["open"].values[0]) / row_i["open"].values[0]

        if (tp < -var_low) and (-var_high < sl):
            if row_i_j["low_time"].values[0] < row_i_j["high_time"].values[0]:
                time_datetime = datetime.strptime(row_i_j["low_time"].values[0],
                                                  "%Y-%m-%d %H:%M:%S") - datetime.strptime(row_i["time"].values[0],
                                                                                           "%Y-%m-%d %H:%M:%S")
                break
            elif row_i_j["high_time"].values[0] < row_i_j["low_time"].values[0]:
                time_datetime = -(datetime.strptime(row_i_j["high_time"].values[0],
                                                    "%Y-%m-%d %H:%M:%S") - datetime.strptime(
                    row_i["time"].values[0], "%Y-%m-%d %H:%M:%S"))
                break

        # IF we touch the tp we break the loop
        elif (tp < -var_low):
            time_datetime = datetime.strptime(row_i_j["low_time"].values[0],
                                              "%Y-%m-%d %H:%M:%S") - datetime.strptime(row_i["time"].values[0],
                                                                                       "%Y-%m-%d %H:%M:%S")
            break

        # IF we touch the sl we break the loop
        elif (-var_high < sl):
            time_datetime = -(
                        datetime.strptime(row_i_j["high_time"].values[0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(
                    row_i["time"].values[0], "%Y-%m-%d %H:%M:%S"))
            break

        else:
            time_datetime = timedelta(0)

    time = time_datetime.total_seconds() / 3600
    return time

def get_ind_barrier(df, nb_row, tp=0.015, sl=-0.015, buy=True):
    if buy:
        time = get_barrier_buy(df, nb_row, tp=tp, sl=sl)
    else:
        time = get_barrier_sell(df, nb_row, tp=tp, sl=sl)
    return time

def get_barrier(df, tp=0.015, sl=-0.015, buy=True):
    # Empty list to contain the labeling
    tpl = list()

    df_copy = df.copy()
    # Loop for to search the labels
    for i in tqdm(range(len(df))):

        # IMPORTANT: try/except for the last row to avoid errors if we don't have found the TP or SL
        try:
            tpl.append(get_ind_barrier(df_copy, i, tp=tp, sl=sl, buy=buy))
        except Exception as e:
            print(e)
            tpl.append(0)

    # Place the label columns in the dataframe
    df_copy["labeling"] = tpl

    return df_copy

def dc_event(Pt, Pext, threshold):
    """
    Compute if we have a POTENTIAL DC event
    """
    var = (Pt - Pext) / Pext
    
    if threshold <= var:
        dc = 1
    elif var <= -threshold:
        dc = -1
    else:
        dc = 0
        
    return dc


def calculate_dc(df, threshold):
    """
    Compute the start and the end of a DC event
    """
    
    # Initialize lists to store DC and OS events
    dc_events_up = []
    dc_events_down = []
    dc_events = []
    os_events = []

    # Initialize the first DC event
    last_dc_price = df["close"][0]
    last_dc_direction = 0  # +1 for up, -1 for down
    
    # Initialize the current Min & Max for the OS events
    min_price = last_dc_price
    max_price = last_dc_price
    idx_min = 0
    idx_max = 0

    
    # Iterate over the price list
    for i, current_price in enumerate(df["close"]):
        
        # Update min & max prices
        try:
            max_price = df["high"].iloc[dc_events[-1][-1]:i].max()
            min_price = df["low"].iloc[dc_events[-1][-1]:i].min()
            idx_min = df["high"].iloc[dc_events[-1][-1]:i].idxmin()
            idx_max = df["low"].iloc[dc_events[-1][-1]:i].idxmax()
        except Exception as e:
            pass
            #print(e, dc_events, i)
            #print("We are computing the first DC")
        
        # Calculate the price change in percentage
        dc_price_min = dc_event(current_price, min_price, threshold)
        dc_price_max = dc_event(current_price, max_price, threshold)
        
        
        # Add the DC event with the right index IF we are in the opposite way
        # Because if we are in the same way, we just increase the OS event size
        if (last_dc_direction!=1) & (dc_price_min==1):
            dc_events_up.append([idx_min, i])
            dc_events.append([idx_min, i])
            last_dc_direction = 1
            
        elif (last_dc_direction!=-1) & (dc_price_max==-1):
            dc_events_down.append([idx_max, i])
            dc_events.append([idx_max, i])
            last_dc_direction = -1
        
    return dc_events_up, dc_events_down, dc_events


def calculate_future_trend(dc_events_down, dc_events_up, df):
    """
    Compute the DC + OS period (trend) using the DC event lists
    """
    
    # Initialize the variables
    trend_events_up = []
    trend_events_down = []
    
    # Verify which event occured first (upward or downward movement)
    
    # If the first event is a downward event
    if dc_events_up[0][0]==0:
        
        # Iterate on the index 
        for i in range(len(dc_events_down)+1):
            
           
            try:
                # Calculate the start and end for each trend
                trend_events_down.append([dc_events_down[i-1][0], dc_events_up[i][0]])
                trend_events_up.append([dc_events_up[i-1][0], dc_events_down[i-1][0]])
            except:
                pass

    # If the first event is a upward event
    elif dc_events_down[0][0]==0:
        
        # Iterate on the index
        for i in range(len(dc_events_up)+1):
            
               
            # Calculate the start and end for each trend
            try:
                trend_events_down.append([dc_events_up[i-1][0], dc_events_down[i][0]])
                trend_events_up.append([dc_events_down[i-1][0], dc_events_up[i-1][0]])
            except:
                pass

        
    return trend_events_down, trend_events_up

def future_DC_market_regime(df, threshold):
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
    trend_events_down, trend_events_up = calculate_future_trend(dc_events_down, dc_events_up, df_copy)
    
    df_copy["future_market_regime"] = np.nan
    for event_up in trend_events_up:
        df_copy.loc[event_up[0], "future_market_regime"] = 0

    for event_down in trend_events_down:
        df_copy.loc[event_down[0], "future_market_regime"] = 1

    df_copy["future_market_regime"] = df_copy["future_market_regime"].fillna(method="ffill")
    
    return df_copy

