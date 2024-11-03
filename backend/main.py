from quart import Quart, jsonify, request
from quart_cors import cors
from controllers.portfolio_manager import PortfolioManager
from algorithms.allocation import Allocation
from algorithms.diversification import Diversification
from algorithms.optimization import Optimization
from algorithms.risk_analysis import RiskAnalysis
from controllers.data_fetcher import (
    fetch_and_save_data,
    fetch_all_data,
    fetch_current_price,
    read_historical_data,
    calculate_profit,
)
from models.transaction import Transaction
from datetime import datetime, timedelta
from prisma import Prisma
import logging

# Initialize the app
app = Quart(__name__)
cors(app)  # Enable CORS

# Initialize Prisma and PortfolioManager instances
prisma = Prisma()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
portfolio_manager = PortfolioManager(prisma)# Initialize as None, we'll set it after connecting

@app.before_serving
async def connect_to_db():
    await prisma.connect()

# Disconnect from the database when the app shuts down
@app.after_serving
async def disconnect_db():
    if prisma.is_connected():
        await prisma.disconnect()


# Decorator to ensure Prisma connection
def ensure_prisma_connection(func):
    async def prisma_connected_wrapper(*args, **kwargs):
        if not prisma.is_connected():
            await prisma.connect()
        return await func(*args, **kwargs)
    
    prisma_connected_wrapper.__name__ = func.__name__
    return prisma_connected_wrapper

# Error handling middleware
@app.errorhandler(Exception)
async def handle_error(error):
    logging.error(f"Unhandled error: {error}")
    return jsonify({
        "error": "An unexpected error occurred",
        "details": str(error)
    }), 500

# API Routes
@app.route('/api/add_asset', methods=['POST'])
@ensure_prisma_connection
async def add_asset():
    data = await request.json
    asset_type = data.get('asset_type', 'stock')
    asset_symbol = data.get('asset_symbol')
    quantity = data.get('quantity')
    price = data.get('price')
    asset_name = data.get('asset_name')
    purchase_date = data.get('purchase_date')

    if not asset_symbol or quantity is None or price is None:
        return jsonify({'error': 'Asset symbol, quantity, and price are required'}), 400

    try:
        asset = await portfolio_manager.add_asset(
            asset_type=asset_type,
            asset_symbol=asset_symbol,
            quantity=float(quantity),
            price=float(price),
            purchase_date=purchase_date,
            asset_name=asset_name
        )
        return jsonify({'success': True, 'asset': asset}), 200
    except Exception as e:
        logging.error(f"Error in add_asset: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/remove_asset', methods=['POST'])
@ensure_prisma_connection
async def remove_asset():
    data = await request.json
    asset_symbol = data.get('asset_symbol')
    quantity = data.get('quantity')

    if not asset_symbol or quantity is None:
        return jsonify({"error": "asset_symbol and quantity are required"}), 400

    try:
        await portfolio_manager.sell_asset(asset_symbol, quantity)
        return jsonify({"message": "Asset removed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error in remove_asset: {e}")
        return jsonify({"error": "Failed to remove asset"}), 500

@app.route('/api/portfolio/total_value', methods=['GET'])
@ensure_prisma_connection
async def get_total_value():
    try:
        total_value = await portfolio_manager.calculate_total_value()
        return jsonify({"total_value": total_value})
    except Exception as e:
        logging.error(f"Error in get_total_value: {e}")
        return jsonify({"error": "Failed to get total portfolio value"}), 500

@app.route('/api/portfolio/allocations', methods=['GET'])
@ensure_prisma_connection
async def get_allocations():
    try:
        allocations = await portfolio_manager.get_allocations()
        return jsonify({"allocations": allocations})
    except Exception as e:
        logging.error(f"Error in get_allocations: {e}")
        return jsonify({"error": "Failed to get allocations"}), 500

@app.route('/api/portfolio/profit/<asset_symbol>', methods=['GET'])
@ensure_prisma_connection
async def get_profit(asset_symbol):
    if not asset_symbol:
        return jsonify({"error": "asset_symbol is required"}), 400

    try:
        profit = await portfolio_manager.calculate_profit(asset_symbol)
        return jsonify({"asset_symbol": asset_symbol, "profit": profit}), 200
    except Exception as e:
        logging.error(f"Error in get_profit for {asset_symbol}: {e}")
        return jsonify({"error": "Failed to calculate profit"}), 500

@app.route('/api/portfolio/transactions', methods=['GET'])
@ensure_prisma_connection
async def get_transactions():
    try:
        transactions = await portfolio_manager.get_transactions()
        return jsonify({"transactions": transactions})
    except Exception as e:
        logging.error(f"Error in get_transactions: {e}")
        return jsonify({"error": "Failed to get transactions"}), 500

@app.route('/api/fetch_all_data', methods=['POST'])
@ensure_prisma_connection
async def fetch_data_for_all_assets():
    try:
        await fetch_all_data()
        return jsonify({"message": "Data fetched for all asset types."}), 200
    except Exception as e:
        logging.error(f"Error in fetch_data_for_all_assets: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/api/allocation', methods=['POST'])
@ensure_prisma_connection
async def calculate_allocation():
    data = await request.json
    assets = data.get('assets')
    
    if not assets:
        return jsonify({"error": "Assets are required for allocation calculation"}), 400

    try:
        allocations = await portfolio_manager.calculate_allocation(assets)
        return jsonify({"allocations": allocations})
    except Exception as e:
        logging.error(f"Error in calculate_allocation: {e}")
        return jsonify({"error": "Failed to calculate allocation"}), 500

@app.route('/api/diversification', methods=['POST'])
@ensure_prisma_connection
async def check_diversification():
    data = await request.json
    assets = data.get('assets')
    
    if not assets:
        return jsonify({"error": "Assets are required for diversification check"}), 400

    try:
        diversification = await portfolio_manager.check_diversification(assets)
        return jsonify({"diversification": diversification})
    except Exception as e:
        logging.error(f"Error in check_diversification: {e}")
        return jsonify({"error": "Failed to check diversification"}), 500
    
@app.route('/api/risk_analysis', methods=['POST'])
@ensure_prisma_connection
async def analyze_risk():
    data = await request.json
    assets = data.get('assets')
    
    if not assets:
        return jsonify({"error": "Assets are required for risk analysis"}), 400

    try:
        risk_metrics = await portfolio_manager.analyze_risk(assets)
        return jsonify({"risk_metrics": risk_metrics})
    except Exception as e:
        logging.error(f"Error in analyze_risk: {e}")
        return jsonify({"error": "Failed to analyze risk"}), 500

@app.route('/api/portfolio/summary', methods=['GET'])
@ensure_prisma_connection
async def get_portfolio_summary():
    try:
        summary = await portfolio_manager.get_portfolio_summary()
        return jsonify(summary)
    except Exception as e:
        logging.error(f"Error in get_portfolio_summary: {e}")
        return jsonify({"error": "Failed to get portfolio summary"}), 500

@app.route('/api/portfolio/assets', methods=['GET'])
@ensure_prisma_connection
async def get_portfolio_assets():
    try:
        assets = await portfolio_manager.get_all_assets()
        return jsonify({"assets": assets})
    except Exception as e:
        logging.error(f"Error in get_portfolio_assets: {e}")
        return jsonify({"error": "Failed to get portfolio assets"}), 500

@app.route('/api/portfolio/asset/<asset_symbol>', methods=['GET'])
@ensure_prisma_connection
async def get_asset_details(asset_symbol):
    try:
        asset_details = await portfolio_manager.get_asset_details(asset_symbol)
        return jsonify(asset_details)
    except Exception as e:
        logging.error(f"Error in get_asset_details for {asset_symbol}: {e}")
        return jsonify({"error": f"Failed to get details for {asset_symbol}"}), 500

@app.route('/api/portfolio/historical-performance', methods=['GET'])
@ensure_prisma_connection
async def get_historical_performance():
    try:
        days = request.args.get('days', default=30, type=int)
        performance = await portfolio_manager.get_historical_performance(days)
        return jsonify({"historical_performance": performance})
    except Exception as e:
        logging.error(f"Error in get_historical_performance: {e}")
        return jsonify({"error": "Failed to get historical performance"}), 500

@app.route('/api/portfolio/rebalance', methods=['POST'])
@ensure_prisma_connection
async def rebalance_portfolio():
    try:
        data = await request.json
        target_allocation = data.get('target_allocation', {})
        rebalancing_suggestions = await portfolio_manager.get_rebalancing_suggestions(target_allocation)
        return jsonify({"rebalancing_suggestions": rebalancing_suggestions})
    except Exception as e:
        logging.error(f"Error in rebalance_portfolio: {e}")
        return jsonify({"error": "Failed to calculate rebalancing suggestions"}), 500

@app.route('/api/market/search', methods=['GET'])
@ensure_prisma_connection
async def search_assets():
    try:
        query = request.args.get('query', '')
        asset_type = request.args.get('type', 'stock')
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        results = await portfolio_manager.search_market_assets(query, asset_type)
        return jsonify({"results": results})
    except Exception as e:
        logging.error(f"Error in search_assets: {e}")
        return jsonify({"error": "Failed to search assets"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)