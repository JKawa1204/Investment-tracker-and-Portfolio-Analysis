# backend/main.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.data_fetcher import fetch_and_save_stock_data, read_stock_data


app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Fetch historical data for a given stock symbol."""
    data = fetch_stock_data(symbol)
    return jsonify(data.to_dict(orient="records"))  # Send DataFrame as JSON

@app.route('/api/stock/<symbol>/price', methods=['GET'])
def get_stock_price(symbol):
    """Fetch the current price for a given stock symbol."""
    price = fetch_current_price(symbol)
    return jsonify({"symbol": symbol, "price": price})

if __name__ == '__main__':
    app.run(debug=True)
