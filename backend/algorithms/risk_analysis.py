# backend/algorithms/risk_analysis.py
from typing import List, Dict
from utils.avl_tree import AVLTree

class RiskAnalysis:
    def __init__(self):
        self.historical_prices = {}  # Initialize empty dictionary

    def set_historical_prices(self, historical_prices: Dict[str, AVLTree]):
        self.historical_prices = historical_prices
        return self

    def calculate_volatility(self, asset_id: str) -> float:
        if asset_id not in self.historical_prices:
            return 0.0

        price_data = self.historical_prices[asset_id].in_order_traversal()
        if len(price_data) < 2:
            return 0.0

        returns = [(price_data[i] - price_data[i - 1]) / price_data[i - 1] 
                   for i in range(1, len(price_data))]

        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        
        return variance ** 0.5  # Standard deviation as volatility

    def generate_alerts(self, threshold: float) -> List[str]:
        if not self.historical_prices:
            return []

        alerts = []
        for asset_id, tree in self.historical_prices.items():
            if self.calculate_volatility(asset_id) > threshold:
                alerts.append(f"High volatility for {asset_id}")

        return alerts