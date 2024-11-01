from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.data_fetcher import fetch_and_save_stock_data, read_stock_data,fetch_current_price
from config.symbols import get_stock_symbols, get_symbol_name  # Import symbols helper functions

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Fetch historical data for a given stock symbol."""
    # Check if the symbol exists
    if symbol not in get_stock_symbols():
        return jsonify({"error": "Symbol not found"}), 404

    data = fetch_and_save_stock_data(symbol)  # Use the correct function name here
    return jsonify(data.to_dict(orient="records"))  # Send DataFrame as JSON

@app.route('/api/stock/<symbol>/price', methods=['GET'])
def get_stock_price(symbol):
    """Fetch the current price for a given stock symbol."""
    # Check if the symbol exists
    if symbol not in get_stock_symbols():
        return jsonify({"error": "Symbol not found"}), 404

    price = fetch_current_price(symbol)
    return jsonify({"symbol": symbol, "price": price})

if __name__ == '__main__':
    app.run(debug=True)
