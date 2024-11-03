from typing import Dict, Optional
from datetime import datetime,timedelta
import logging
from prisma import Prisma
from config.asset_service import get_asset_name
from controllers.data_fetcher import fetch_current_price
from models.transaction import Transaction
from algorithms.optimization import Optimization
from algorithms.allocation import Allocation
from algorithms.diversification import Diversification
from algorithms.risk_analysis import RiskAnalysis
from utils.queue import Queue

# Initialize Prisma client
prisma = Prisma()

# Constants for transaction types
TRANSACTION_TYPE_BUY = "buy"
TRANSACTION_TYPE_SELL = "sell"

class PortfolioManager:
    def __init__(self, prisma_client):
        self.prisma = prisma_client
        self.recent_transactions = []
        self.allocation = Allocation()
        self.diversification = Diversification()
        self.optimization = Optimization()
        self.risk_analysis = RiskAnalysis()

    async def load_recent_transactions(self):
        try:
            recent_transactions = await self.prisma.transaction.find_many(
                order=[{"date": "desc"}],
                take=10
            )
            self.recent_transactions = recent_transactions
        except Exception as e:
            logging.error(f"Error loading recent transactions: {str(e)}")
            self.recent_transactions = []

    async def ensure_connected(self):
        """Ensure Prisma client is connected before querying."""
        if not prisma.is_connected():
            await prisma.connect()

    async def log_transaction(self, transaction: Transaction):
        """Logs a transaction to the database."""
        try:
            await prisma.transaction.create(
                data={
                    "assetId": transaction.asset_symbol,
                    "type": transaction.transaction_type,
                    "quantity": transaction.amount,
                    "price": transaction.price,
                    "createdAt": transaction.purchase_date,
                }
            )
        except Exception as e:
            logging.error(f"Error logging transaction: {e}")

    async def add_asset(
    self,
    asset_type: str,
    asset_symbol: str,
    quantity: float,
    price: float,
    purchase_date: Optional[str] = None,
    asset_name: Optional[str] = None
):
        """Adds or updates an asset in the portfolio and logs the purchase transaction."""
        await self.ensure_connected()
    
        asset_name = asset_name or await get_asset_name(asset_symbol)
        purchase_date = purchase_date or datetime.now().isoformat()

        try:
        # Check if asset exists
            existing_asset = await prisma.asset.find_first(
                where={
                "symbol": asset_symbol
                }
            )

            if existing_asset:
                # Update existing asset
                asset = await prisma.asset.update(
                    where={
                        "id": existing_asset.id
                    },
                    data={
                    "quantity": existing_asset.quantity + quantity,
                    "price": price
                }
                )
            else:
            # Create new asset
                asset = await prisma.asset.create(
                    data={
                    "symbol": asset_symbol,
                    "name": asset_name,
                    "assetType": asset_type,
                    "quantity": quantity,
                    "price": price,
                }
            )

        # Log the transaction
            transaction = Transaction(
            asset_symbol=asset_symbol,
            transaction_type=TRANSACTION_TYPE_BUY,
            amount=quantity,
            price=price,
            purchase_date=purchase_date
            )
            await self.log_transaction(transaction)
        
            return asset

        except Exception as e:
            logging.error(f"An error occurred while adding asset: {e}")
            raise

    async def remove_asset(self, asset_symbol: str, quantity: float):
        """Removes an asset from the portfolio, logs the sale transaction, and updates the database."""
        await self.ensure_connected()

        try:
            asset = await prisma.asset.find_first(where={"symbol": asset_symbol})

            if not asset:
                raise ValueError("Asset not found in the portfolio")
            if asset.quantity < quantity:
                raise ValueError("Not enough quantity to sell")

            current_price = await fetch_current_price(asset_symbol)

            updated_asset = await prisma.asset.update(
                where={"id": asset.id},
                data={"quantity": asset.quantity - quantity}
            )

            # Log the sale transaction
            transaction = Transaction(
                asset_symbol=asset_symbol,
                transaction_type=TRANSACTION_TYPE_SELL,
                amount=quantity,
                price=current_price,
                purchase_date=datetime.now().isoformat()
            )
            await self.log_transaction(transaction)

            # Update the local portfolio data
            self.assets[asset_symbol]["quantity"] -= quantity
            if self.assets[asset_symbol]["quantity"] <= 0:
                del self.assets[asset_symbol]

            if updated_asset.quantity == 0:
                await prisma.asset.delete(where={"id": updated_asset.id})

            return updated_asset

        except Exception as e:
            logging.error(f"Error removing asset {asset_symbol}: {e}")
            raise

    def add_dividend(self, asset_symbol: str, dividend: float):
        """Add dividend to the queue for reinvestment."""
        self.dividends.enqueue((asset_symbol, dividend))

    async def process_dividends(self):
        """Process and reinvest dividends."""
        await self.ensure_connected()
        while not self.dividends.is_empty():
            asset_symbol, dividend = self.dividends.dequeue()
            current_price = await fetch_current_price(asset_symbol)
            quantity = dividend / current_price
            await self.add_asset(asset_type="stock", asset_symbol=asset_symbol, quantity=quantity, price=current_price)

    async def rebalance_portfolio(self, target_allocations: Dict[str, float]):
        """Rebalance the portfolio based on target allocations."""
        await self.ensure_connected()
        current_allocations = await self.get_allocations()
        optimization = Optimization(current_allocations, target_allocations)
        adjustments = optimization.rebalance()

        for asset_symbol, adjustment in adjustments.items():
            price = await fetch_current_price(asset_symbol)
            if adjustment > 0:
                await self.add_asset(asset_type="stock", asset_symbol=asset_symbol, quantity=adjustment, price=price)
            elif adjustment < 0:
                await self.remove_asset(asset_symbol, -adjustment)

    async def get_total_value(self) -> float:
        """Calculates the total value of the portfolio based on current prices."""
        await self.ensure_connected()
        total_value = 0.0

        for asset_symbol, asset in self.assets.items():
            current_price = await fetch_current_price(asset_symbol)
            total_value += asset["quantity"] * current_price
        return total_value

    async def get_allocations(self) -> Dict[str, float]:
        """Calculates the allocation percentage of each asset in the portfolio."""
        total_value = await self.get_total_value()
        if total_value == 0:
            return {}

        allocations = {
            asset_symbol: (await fetch_current_price(asset_symbol) * asset["quantity"]) / total_value
            for asset_symbol, asset in self.assets.items()
        }
        return allocations

    async def get_portfolio_summary(self):
        """Get a summary of the portfolio including total value and individual asset details."""
        await self.ensure_connected()
        summary = {'total_value': 0, 'assets': {}}
        
        for asset_symbol, asset_data in self.assets.items():
            current_price = await fetch_current_price(asset_symbol)
            asset_value = current_price * asset_data['quantity']
            summary['total_value'] += asset_value
            summary['assets'][asset_symbol] = {
                'name': await get_asset_name(asset_symbol),
                'quantity': asset_data['quantity'],
                'current_price': current_price,
                'value': asset_value
            }
        return summary

    async def get_asset_performance(self, asset_symbol: str):
        """Get the performance of a specific asset in the portfolio."""
        await self.ensure_connected()
        asset = self.assets.get(asset_symbol)
        
        if not asset:
            raise ValueError("Asset not found in portfolio")
        
        current_price = await fetch_current_price(asset_symbol)
        purchase_price = asset['price']
        performance = {
            'name': await get_asset_name(asset_symbol),
            'quantity': asset['quantity'],
            'purchase_price': purchase_price,
            'current_price': current_price,
            'total_value': current_price * asset['quantity'],
            'profit_loss': (current_price - purchase_price) * asset['quantity'],
            'percent_change': ((current_price - purchase_price) / purchase_price) * 100
        }
        return performance

    async def get_transaction_history(self, asset_symbol: Optional[str] = None):
        """Fetches the transaction history from the database."""
        await self.ensure_connected()
        try:
            where = {"assetId": asset_symbol} if asset_symbol else {}
            transactions = await prisma.transaction.find_many(
                where=where,
                order={"createdAt": "desc"}
            )
            return transactions
        except Exception as e:
            logging.error(f"Error fetching transaction history: {e}")
            return []
        
    async def log_transaction(self, transaction: Transaction):
        """Logs a transaction to the database and in-memory history."""
        try:
            await prisma.transaction.create(
                data={
                    "assetId": transaction.asset_symbol,
                    "type": transaction.transaction_type,
                    "quantity": transaction.amount,
                    "price": transaction.price,
                    "createdAt": transaction.purchase_date,
                }
            )
            self.transaction_history.add_transaction(transaction)
        except Exception as e:
            logging.error(f"Error logging transaction: {e}")

    async def get_transaction_history(self, asset_symbol: Optional[str] = None, 
                                      start_date: Optional[datetime] = None,
                                      end_date: Optional[datetime] = None,
                                      use_cache: bool = True):
        """Fetches the transaction history from the database or in-memory cache."""
        await self.ensure_connected()
        try:
            if use_cache:
                if start_date or end_date:
                    return self.transaction_history.get_transactions_by_date_range(start_date, end_date)
                return self.transaction_history.get_transactions(asset_symbol)
            else:
                where = {}
                if asset_symbol:
                    where["assetId"] = asset_symbol
                if start_date:
                    where["createdAt"] = {"gte": start_date}
                if end_date:
                    where["createdAt"] = {"lte": end_date}
                transactions = await prisma.transaction.find_many(
                    where=where,
                    order={"createdAt": "desc"}
                )
                return transactions
        except Exception as e:
            logging.error(f"Error fetching transaction history: {e}")
            return []

    async def load_recent_transactions(self, days: int = 30):
        """Load recent transactions into memory."""
        start_date = datetime.now() - timedelta(days=days)
        recent_transactions = await prisma.transaction.find_many(
            where={'createdAt': {'gte': start_date}},
            order={'createdAt': 'desc'}
        )
        
        for tx in recent_transactions:
            transaction = Transaction(
                asset_symbol=tx.assetId,
                transaction_type=tx.type,
                amount=tx.quantity,
                price=tx.price,
                purchase_date=tx.createdAt
            )
            self.transaction_history.add_transaction(transaction)


    async def disconnect(self):
        await prisma.disconnect()