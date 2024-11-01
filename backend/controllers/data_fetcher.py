import yfinance as yf
import pandas as pd
import os
from config.symbols import get_stock_symbols, get_bond_symbols, get_crypto_symbols

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/historical_data.csv')

def fetch_and_save_data(symbol, asset_type="stock"):
    """
    Fetch and save historical data for a given symbol.
    Supports stocks, bonds, and cryptos.
    
    Args:
        symbol (str): The asset symbol.
        asset_type (str): Type of asset, e.g., 'stock', 'bond', 'crypto'.
    
    Returns:
        pd.DataFrame: The fetched historical data.
    """
    valid_symbols = {
        "stock": get_stock_symbols(),
        "bond": get_bond_symbols(),
        "crypto": get_crypto_symbols(),
    }

    if symbol not in valid_symbols.get(asset_type, []):
        print(f"Invalid symbol: {symbol} for asset type: {asset_type}")
        return None

    # Fetch data from Yahoo Finance
    asset = yf.Ticker(symbol)
    data = asset.history(period="1y")
    data['Symbol'] = symbol  # Add symbol column for easy lookup

    # Append data to CSV or create it if it doesn’t exist
    if not os.path.exists(DATA_PATH):
        data.to_csv(DATA_PATH, mode='w', index=True)
    else:
        data.to_csv(DATA_PATH, mode='a', header=False, index=True)

    print(f"Data for {symbol} ({asset_type}) has been saved to {DATA_PATH}.")
    return data

def fetch_current_price(symbol, asset_type="stock"):
    """
    Fetches the latest price for a given asset symbol.
    
    Args:
        symbol (str): The asset symbol.
        asset_type (str): Type of asset, e.g., 'stock', 'bond', 'crypto'.
    
    Returns:
        float or None: Latest close price if symbol is valid, else None.
    """
    valid_symbols = {
        "stock": get_stock_symbols(),
        "bond": get_bond_symbols(),
        "crypto": get_crypto_symbols(),
    }

    if symbol not in valid_symbols.get(asset_type, []):
        print(f"Invalid symbol: {symbol} for asset type: {asset_type}")
        return None

    asset = yf.Ticker(symbol)
    try:
        current_price = asset.history(period="1d")['Close'].iloc[-1]
        return current_price
    except (IndexError, KeyError):
        print(f"Failed to fetch current price for {symbol}")
        return None

def read_historical_data(symbol):
    """
    Reads historical data for a symbol from `historical_data.csv`.
    
    Args:
        symbol (str): The asset symbol.
    
    Returns:
        pd.DataFrame: Dataframe containing historical prices for the given symbol.
    """
    if not os.path.exists(DATA_PATH):
        print(f"No historical data found at {DATA_PATH}.")
        return None

    data = pd.read_csv(DATA_PATH)
    symbol_data = data[data['Symbol'] == symbol]

    if symbol_data.empty:
        print(f"No data found for symbol {symbol} in historical_data.csv")
        return None

    return symbol_data

def calculate_profit(symbol, purchase_price):
    """
    Calculates the profit based on the purchase price and current market price.
    
    Args:
        symbol (str): The asset symbol.
        purchase_price (float): The price at which the asset was purchased.
    
    Returns:
        float: The calculated profit (current price - purchase price).
    """
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print(f"Could not fetch current price for {symbol}.")
        return None

    profit = current_price - purchase_price
    print(f"Profit for {symbol} = {profit}")
    return profit

# Utility to fetch data for all configured symbols
def fetch_all_data():
    """
    Fetches and saves data for all symbols across asset types.
    """
    for asset_type, symbols in [("stock", get_stock_symbols()), ("bond", get_bond_symbols()), ("crypto", get_crypto_symbols())]:
        for symbol in symbols:
            fetch_and_save_data(symbol, asset_type)
    print("Data fetched for all configured symbols.")
