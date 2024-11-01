# backend/controllers/portfolio_manager.py
from typing import Dict, List
from backend.models.transaction import Transaction
from backend.algorithms.optimization import Optimization
from backend.utils.queue import Queue

class PortfolioManager:
    def __init__(self):
        self.transactions = []
        self.dividends = Queue()  # Queue for dividend reinvestment
        self.portfolio = {}  # {asset_id: quantity}

    def buy_asset(self, asset_id: str, amount: float):
        self.portfolio[asset_id] = self.portfolio.get(asset_id, 0) + amount
        transaction = Transaction(asset_id, "buy", amount)
        self.transactions.append(transaction)
        
    def sell_asset(self, asset_id: str, amount: float):
        if asset_id in self.portfolio and self.portfolio[asset_id] >= amount:
            self.portfolio[asset_id] -= amount
            transaction = Transaction(asset_id, "sell", amount)
            self.transactions.append(transaction)

    def add_dividend(self, asset_id: str, dividend: float):
        self.dividends.enqueue((asset_id, dividend))
        
    def process_dividends(self):
        while not self.dividends.is_empty():
            asset_id, dividend = self.dividends.dequeue()
            if asset_id in self.portfolio:
                self.buy_asset(asset_id, dividend)

    def rebalance_portfolio(self, target_allocations: Dict[str, float]):
        optimization = Optimization(self.portfolio, target_allocations)
        adjustments = optimization.rebalance()
        for asset_id, adjustment in adjustments.items():
            self.buy_asset(asset_id, adjustment) if adjustment > 0 else self.sell_asset(asset_id, -adjustment)
