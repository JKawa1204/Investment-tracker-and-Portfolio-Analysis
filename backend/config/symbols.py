stocks = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    # Other stocks...
}

bonds = {
    "US10Y": "10-Year Treasury Bond",
    "CORP1": "Corporate Bond A",
    # Other bonds...
}

cryptos = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    # Other cryptos...
}

def get_asset_name(asset_type, symbol):
    if asset_type == "stock":
        return stocks.get(symbol, "Unknown Stock")
    elif asset_type == "bond":
        return bonds.get(symbol, "Unknown Bond")
    elif asset_type == "crypto":
        return cryptos.get(symbol, "Unknown Crypto")
    else:
        return "Unknown Asset Type"

def get_stock_symbols():
    return list(stocks.keys())

def get_bond_symbols():
    return list(bonds.keys())

def get_crypto_symbols():
    return list(cryptos.keys())
