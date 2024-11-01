# backend/config/symbols.py

STOCK_SYMBOLS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com, Inc.",
    "TSLA": "Tesla, Inc.",
    # Add more symbols as needed
}

def get_stock_symbols():
    """Return a list of available stock symbols."""
    return list(STOCK_SYMBOLS.keys())

def get_symbol_name(symbol):
    """Return the full name of the company for a given symbol."""
    return STOCK_SYMBOLS.get(symbol, "Unknown Symbol")
