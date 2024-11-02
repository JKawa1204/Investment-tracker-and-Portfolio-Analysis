from typing import Dict
from backend.models.transaction import Transaction
from backend.algorithms.optimization import Optimization
from backend.utils.queue import Queue  # Custom queue implementation
from config.symbols import get_stock_symbols, get_symbol_name
from prisma.models import Transaction as PrismaTransaction
from prisma.models import Asset as PrismaAsset
from models.portfolio import Portfolio  # Import the Portfolio class

class PortfolioManager:
    def __init__(self):
        # Instantiate Portfolio for in-memory management and Prisma transactions
        self.portfolio = Portfolio()  # Portfolio instance for asset tracking and database logging
        self.dividends = Queue()  # Queue to manage dividends for reinvestment

    async def buy_asset(self, asset_id: str, amount: float, price: float):
        """Handles asset purchase and logs transaction."""
        await self.portfolio.add_asset("stock", Asset(id=asset_id, name="", sector="", price=price), amount, price)

    async def sell_asset(self, asset_id: str, amount: float, price: float):
        """Handles asset sale and logs transaction, ensuring sufficient quantity."""
        try:
            await self.portfolio.remove_asset("stock", asset_id, amount, price)
        except ValueError as e:
            raise ValueError("Insufficient quantity to sell.") from e

    def add_dividend(self, asset_id: str, dividend: float):
        """Adds dividends to the queue for reinvestment."""
        self.dividends.enqueue((asset_id, dividend))
        
    async def process_dividends(self):
        """Processes queued dividends and reinvests them in respective assets."""
        while not self.dividends.is_empty():
            asset_id, dividend = self.dividends.dequeue()
            if asset_id in self.portfolio.assets:
                await self.buy_asset(asset_id, dividend, price=0)  # Assuming dividends reinvest at $0

    async def rebalance_portfolio(self, target_allocations: Dict[str, float]):
        """Rebalances portfolio to match target allocations using Optimization."""
        current_allocations = await self.portfolio.get_allocations()
        optimization = Optimization(current_allocations, target_allocations)
        adjustments = optimization.rebalance()

        for asset_id, adjustment in adjustments.items():
            price = await fetch_current_price(asset_id)  # Fetch the current price for accurate rebalancing
            if adjustment > 0:
                await self.buy_asset(asset_id, adjustment, price)
            else:
                await self.sell_asset(asset_id, -adjustment, price)
                
    async def get_total_value(self) -> float:
        """Calculates total value of the portfolio."""
        return await self.portfolio.get_total_value()

    async def get_allocations(self) -> Dict[str, float]:
        """Fetches allocation percentages for each asset."""
        return await self.portfolio.get_allocations()

    async def get_transaction_history(self) -> list:
        """Retrieves transaction history from the database."""
        return await self.portfolio.get_transaction_history()
