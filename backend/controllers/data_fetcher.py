import yfinance as yf
import pandas as pd
import asyncio
from prisma import Prisma  # Import Prisma client
from config.asset_service import get_asset_types


async def fetch_and_save_data(symbol, asset_type="stock"):
    """
    Fetch and save historical data for a given symbol to the database.
    Supports stocks, bonds, and cryptos.

    Args:
        symbol (str): The asset symbol.
        asset_type (str): Type of asset, e.g., 'stock', 'bond', 'crypto'.

    Returns:
        pd.DataFrame: The fetched historical data.
    """
    # Fetch data from Yahoo Finance
    asset = yf.Ticker(symbol)
    data = asset.history(period="1y")
    data['Symbol'] = symbol  # Add symbol column for easy lookup

    # Insert historical data into the Prisma database
    for date, row in data.iterrows():
        await db.historicaldata.create({
            'data': {
                'date': date,
                'closePrice': row['Close'],
                'asset': {
                    'connect': {'symbol': symbol}  # Link to the Asset by symbol
                }
            }
        })

    print(f"Data for {symbol} ({asset_type}) has been saved to the database.")
    return data

async def fetch_current_price(symbol):
    """
    Fetches the latest price for a given asset symbol.

    Args:
        symbol (str): The asset symbol.

    Returns:
        float or None: Latest close price if symbol is valid, else None.
    """
    asset = yf.Ticker(symbol)
    try:
        current_price = asset.history(period="1d")['Close'].iloc[-1]
        return current_price
    except (IndexError, KeyError):
        print(f"Failed to fetch current price for {symbol}")
        return None

async def read_historical_data(symbol):
    """
    Reads historical data for a symbol from the database.

    Args:
        symbol (str): The asset symbol.

    Returns:
        list: List containing historical prices for the given symbol.
    """
    historical_data = await db.historicaldata.find_many(where={'asset': {'symbol': symbol}})
    if not historical_data:
        print(f"No data found for symbol {symbol} in the database")
        return None

    return historical_data

async def calculate_profit(symbol, purchase_price):
    """
    Calculates the profit based on the purchase price and current market price.

    Args:
        symbol (str): The asset symbol.
        purchase_price (float): The price at which the asset was purchased.

    Returns:
        float: The calculated profit (current price - purchase price).
    """
    current_price = await fetch_current_price(symbol)
    if current_price is None:
        print(f"Could not fetch current price for {symbol}.")
        return None

    profit = current_price - purchase_price
    print(f"Profit for {symbol} = {profit}")
    return profit

async def fetch_all_data():
    """
    Fetches and saves data for all assets across types, using symbols from the Asset model.
    """
    assets = await db.asset.find_many()  # Fetch all assets from the database
    for asset in assets:
        await fetch_and_save_data(asset.symbol, asset.assetType)
    print("Data fetched for all configured symbols.")

# To call the fetch_all_data function asynchronously:
# asyncio.run(fetch_all_data())
