import yfinance as yf
import pandas as pd
import logging

# Get historical stock data
def get_historical_data(ticker, timescale):
    try:
        if timescale == 'day':
            prd = '1d'
            itrvl = '1m'
        elif timescale == 'week':
            prd = '5d'
            itrvl = '1d'
        elif timescale == 'month':
            prd = '1mo'
            itrvl = '1d'
        elif timescale == 'year':
            prd = '1y'
            itrvl = '1d'
            
        # Fetch historical stock data using yfinance
        data = yf.download(ticker, period=prd, interval=itrvl, auto_adjust=True, progress=False)
        return data
    except Exception as e: 
        logging.info(f'Error getting data for {ticker}: {e}')
        return None

# Get stock closing prices
def get_close_prices(ticker, timescale='day'):
    data = get_historical_data(ticker, timescale)
    close_prices = data['Close']
    return close_prices

# Calculate Bollinger Bands
def calculate_bollinger_bands(close, window_size=20, num_std_dev=2):
    rolling_mean = close.rolling(window=window_size).mean()
    rolling_std = close.rolling(window=window_size).std()

    # Calculate upper and lower Bollinger Bands
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std
    return upper_band, lower_band

# Return close price time series with Bollinger Bands
def get_close_with_bands(ticker, timescale='day'):
    close = get_close_prices(ticker, timescale)
    upper_band, lower_band = calculate_bollinger_bands(close)
    dataframe = pd.DataFrame({'Close': close, 'Upper Band': upper_band, 'Lower Band': lower_band})
    dataframe.reset_index(inplace=True)
    return dataframe[20:]

#data = get_historical_data('SPY', 'day')
#logging.info(data)