from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from backend.controllers.portfolio_manager import PortfolioManager
from backend.controllers.data_fetcher import fetch_all_data, fetch_current_price, read_historical_data
from backend.algorithms.allocation import Allocation
from backend.algorithms.diversification import Diversification
from backend.algorithms.optimization import Optimization
from backend.algorithms.risk_analysis import RiskAnalysis

app = Flask(__name__)
CORS(app)

# Initialize PortfolioManager
portfolio_manager = PortfolioManager()

@app.route('/api/add_asset', methods=['POST'])
def add_asset():
    data = request.json
    asset_id = data['asset_id']
    asset_type = data.get('asset_type', 'stock')
    asset_name = data['name']
    sector = data['sector']
    quantity = data['quantity']
    price = data['price']

    asyncio.run(portfolio_manager.buy_asset(asset_id, quantity, price))
    return jsonify({"message": "Asset added successfully"}), 201

@app.route('/api/remove_asset', methods=['POST'])
def remove_asset():
    data = request.json
    asset_id = data['asset_id']
    quantity = data['quantity']
    price = data['price']

    try:
        asyncio.run(portfolio_manager.sell_asset(asset_id, quantity, price))
        return jsonify({"message": "Asset removed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/portfolio/total_value', methods=['GET'])
def get_total_value():
    total_value = asyncio.run(portfolio_manager.get_total_value())
    return jsonify({"total_value": total_value})

@app.route('/api/portfolio/allocations', methods=['GET'])
def get_allocations():
    allocations = asyncio.run(portfolio_manager.get_allocations())
    return jsonify({"allocations": allocations})

@app.route('/api/portfolio/profit/<asset_id>', methods=['GET'])
def calculate_profit(asset_id):
    purchase_price = request.args.get('purchase_price', type=float)
    profit = asyncio.run(portfolio_manager.calculate_profit(asset_id, purchase_price))
    return jsonify({"asset_id": asset_id, "profit": profit})

@app.route('/api/portfolio/transactions', methods=['GET'])
def get_transactions():
    asset_id = request.args.get('asset_id')
    transactions = asyncio.run(portfolio_manager.get_transaction_history(asset_id))
    return jsonify(transactions)

@app.route('/api/fetch_all_data', methods=['POST'])
def fetch_data_for_all_assets():
    asyncio.run(fetch_all_data())
    return jsonify({"message": "Data fetched for all asset types."}), 200

@app.route('/api/allocation', methods=['POST'])
def calculate_allocation():
    assets = request.json['assets']
    allocation_algo = Allocation(assets)
    allocations = allocation_algo.calculate_allocation()
    return jsonify({"allocations": allocations})

@app.route('/api/diversification', methods=['POST'])
def check_diversification():
    assets = request.json['assets']
    diversification_algo = Diversification(assets)
    diversification = diversification_algo.check_diversification()
    return jsonify({"diversification": diversification})

@app.route('/api/optimization', methods=['POST'])
def rebalance_portfolio():
    target_allocations = request.json['target_allocations']
    adjustments = asyncio.run(portfolio_manager.rebalance_portfolio(target_allocations))
    return jsonify({"adjustments": adjustments})

@app.route('/api/risk_alerts', methods=['POST'])
def generate_risk_alerts():
    threshold = request.json.get('threshold', 0.05)
    historical_prices = read_historical_data()
    risk_analysis = RiskAnalysis(historical_prices)
    alerts = risk_analysis.generate_alerts(threshold)
    return jsonify({"alerts": alerts})

@app.route('/api/dividends', methods=['POST'])
def add_dividend():
    data = request.json
    asset_id = data['asset_id']
    dividend = data['dividend']

    portfolio_manager.add_dividend(asset_id, dividend)
    return jsonify({"message": "Dividend added successfully"}), 200

@app.route('/api/process_dividends', methods=['POST'])
def process_dividends():
    asyncio.run(portfolio_manager.process_dividends())
    return jsonify({"message": "Dividends processed successfully"}), 200

@app.route('/api/transaction_history', methods=['GET'])
def transaction_history():
    asset_id = request.args.get("asset_id")
    history = asyncio.run(portfolio_manager.get_transaction_history(asset_id))
    return jsonify({"transaction_history": history})

if __name__ == '__main__':
    app.run(debug=True)
