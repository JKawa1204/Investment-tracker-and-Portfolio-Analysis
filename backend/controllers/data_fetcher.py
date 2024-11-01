# backend/controllers/data_fetcher.py

import yfinance as yf
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/historical_data.csv')

def fetch_and_save_stock_data(symbol):
    """
    Fetch historical stock data from Yahoo Finance and save to historical_data.csv.
    If the file doesn't exist, it will create it; otherwise, it appends new data.

    Args:
        symbol (str): The stock symbol to fetch (e.g., "AAPL").

    Returns:
        pd.DataFrame: The fetched historical stock data.
    """
    # Fetch historical data using yfinance
    stock = yf.Ticker(symbol)
    data = stock.history(period="1y")
    data['Symbol'] = symbol  # Add a column to identify the stock symbol

    # If file does not exist, save with headers; else append
    if not os.path.exists(DATA_PATH):
        data.to_csv(DATA_PATH, mode='w', index=True)
    else:
        data.to_csv(DATA_PATH, mode='a', header=False, index=True)
    
    print(f"Data for {symbol} has been fetched and saved.")
    return data

def read_stock_data(symbol):
    """
    Reads stock data for a symbol from historical_data.csv if available.

    Args:
        symbol (str): The stock symbol to read (e.g., "AAPL").

    Returns:
        pd.DataFrame or None: DataFrame with stock data if found, else None.
    """
    if os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
        if symbol in data['Symbol'].values:
            return data[data['Symbol'] == symbol]
    return None  # Return None if data is not found
