# backend/algorithms/risk_analysis.py
from typing import List, Dict
from backend.utils.avl_tree import AVLTree

class RiskAnalysis:
    def __init__(self, historical_prices: Dict[str, AVLTree]):
        self.historical_prices = historical_prices  # Each asset's prices are stored in AVL trees

    def calculate_volatility(self, asset_id: str) -> float:
        price_data = self.historical_prices[asset_id].in_order_traversal()
        returns = [(price_data[i] - price_data[i - 1]) / price_data[i - 1] for i in range(1, len(price_data))]

        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        
        return variance ** 0.5  # Standard deviation as volatility

    def generate_alerts(self, threshold: float) -> List[str]:
        alerts = []
        for asset_id, tree in self.historical_prices.items():
            if self.calculate_volatility(asset_id) > threshold:
                alerts.append(f"High volatility for {asset_id}")

        return alerts
