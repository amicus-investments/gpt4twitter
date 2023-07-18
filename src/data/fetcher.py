from pandas_datareader import data as pddata
from sklearn.preprocessing import MinMaxScaler
import os, datetime
import numpy as np
from collections import deque

fred_api_key = os.getenv("FRED_API_KEY")

# Define the list of indicators
indicators = ['FEDFUNDS']

def fetch_data():
    # Define the lookback period (1 year)
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)

    # Fetch the data and normalize if needed
    economic_data = []
    natural=[]
    for indicator in indicators:
        print(f'Processing {indicator}')
        series = pddata.DataReader(indicator, "fred", start, end, api_key=fred_api_key)

        # Handle empty series by increasing lookback period
        while series.empty:
            start -= datetime.timedelta(days=365)  # Increase lookback period by 1 year
            series = pddata.DataReader(indicator, "fred", start, end, api_key=fred_api_key)

        # rescale all data to logit range
        scaler = MinMaxScaler()
        for indicator in series:
            scaled_series = scaler.fit_transform(series[indicator].values.reshape(-1, 1))
            economic_data.append(series.iloc[-1].values[0]) # only grab last point

        # append the natural text in a list
        natural.append(f'The most recent reported value of {indicator} from FRED is: {series.iloc[-1].values[0]}.  The normalized to 0 to 1 value over the past year is {scaled_series[-1]}.')

    economic_data=[float(e) for e in economic_data]

    # Check if economic data has changed
    new_data = False
    old_economic_data = None
    if os.path.exists('data/economic_data.txt'):
        with open('data/economic_data.txt', 'r') as f:
            old_economic_data = [float(line.rstrip('\n')) for line in f]
    if old_economic_data != economic_data:
        new_data = True
        print('New economic data detected!')
                
    # Save the new economic data
    with open('data/economic_data.txt', 'w') as f:
        for data_point in economic_data:
            f.write(str(data_point) + '\n')
            
    # form the FRED data in natural language form
    frednat = ' '.join(natural)

    return frednat, new_data
