from flask import Flask, jsonify, request
from flask_cors import CORS
from models.portfolio import Portfolio
from models.asset import Asset
from algorithms.allocation import Allocation
from algorithms.diversification import Diversification
from algorithms.optimization import Optimization
from algorithms.risk_analysis import RiskAnalysis
from controllers.data_fetcher import fetch_and_save_data, fetch_all_data, fetch_current_price,read_historical_data,calculate_profit

app = Flask(__name__)
CORS(app)

portfolio = Portfolio()  # Global portfolio instance

@app.route('/api/add_asset', methods=['POST'])
def add_asset():
    data = request.json
    asset_type = data.get('asset_type', 'stock')  # Default to "stock" if not specified
    asset_id = data['asset_id']
    asset_name = data['name']
    sector = data['sector']
    quantity = data['quantity']
    price = data['price']
    
    asset = Asset(id=asset_id, name=asset_name, sector=sector, price=price)
    portfolio.add_asset(asset_type, asset, quantity, price)
    return jsonify({"message": "Asset added successfully"}), 201

@app.route('/api/remove_asset', methods=['POST'])
def remove_asset():
    data = request.json
    asset_type = data.get('asset_type', 'stock')  # Include asset_type, default to "stock"
    asset_id = data['asset_id']
    quantity = data['quantity']
    price = data['price']
    
    try:
        portfolio.remove_asset(asset_type, asset_id, quantity, price)
        return jsonify({"message": "Asset removed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/portfolio/total_value', methods=['GET'])
def get_total_value():
    total_value = portfolio.get_total_value()
    return jsonify({"total_value": total_value})

@app.route('/api/portfolio/allocations', methods=['GET'])
def get_allocations():
    allocations = portfolio.get_allocations()
    return jsonify({"allocations": allocations})

@app.route('/api/portfolio/profit/<asset_id>', methods=['GET'])
def calculate_profit(asset_id):
    profit = calculate_profit("stock", asset_id)  # Assume default "stock" type
    return jsonify({"asset_id": asset_id, "profit": profit})

@app.route('/api/portfolio/transactions', methods=['GET'])
def get_transactions():
    asset_id = request.args.get('asset_id')
    transactions = portfolio.get_transaction_history()
    if asset_id:
        transactions = [t for t in transactions if t['asset_id'] == asset_id]
    return jsonify(transactions)

@app.route('/api/fetch_all_data', methods=['POST'])
def fetch_data_for_all_assets():
    """
    Triggers fetching of data for all configured symbols (stocks, bonds, cryptos).
    """
    fetch_all_data()
    return jsonify({"message": "Data fetched for all asset types."}), 200

@app.route('/api/allocation', methods=['POST'])
def calculate_allocation():
    assets = request.json['assets']  # List of assets with 'id' and 'priority'
    allocation_algo = Allocation(assets)
    allocations = allocation_algo.calculate_allocation()
    return jsonify({"allocations": allocations})

@app.route('/api/diversification', methods=['POST'])
def check_diversification():
    assets = request.json['assets']  # List of assets with 'id' and 'sector'
    diversification_algo = Diversification(assets)
    diversification = diversification_algo.check_diversification()
    return jsonify({"diversification": diversification})

@app.route('/api/rebalance', methods=['POST'])
def rebalance_portfolio():
    target_allocations = request.json['target_allocations']  # Expected {asset_id: target_weight}
    current_allocations = portfolio.get_allocations()
    
    optimization_algo = Optimization(current_allocations, target_allocations)
    adjustments = optimization_algo.rebalance()
    
    for asset_id, adjustment in adjustments.items():
        asset_type = portfolio.get_asset_type(asset_id)  # Assume this function exists or adapt it
        if adjustment > 0:
            price = fetch_current_price(asset_id)  # Fetch current price for rebalancing
            portfolio.add_asset(asset_type, Asset(asset_id, "", "", price), adjustment, price)
        else:
            portfolio.remove_asset(asset_type, asset_id, -adjustment, price)
    
    return jsonify({"adjustments": adjustments})

@app.route('/api/risk_alerts', methods=['POST'])
def generate_risk_alerts():
    threshold = request.json['threshold']
    historical_prices =   read_historical_data()# Replace with actual data retrieval logic
    
    risk_analysis = RiskAnalysis(historical_prices)
    alerts = risk_analysis.generate_alerts(threshold)
    
    return jsonify({"alerts": alerts})

@app.route('/api/transaction_history', methods=['GET'])
def transaction_history():
    asset_id = request.args.get("asset_id")
    history = portfolio.get_transaction_history()
    if asset_id:
        history = [h for h in history if h["asset_id"] == asset_id]
    return jsonify({"transaction_history": history})

if __name__ == '__main__':
    app.run(debug=True)
