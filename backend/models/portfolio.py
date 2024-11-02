import os
from typing import Dict
from prisma import Prisma  # Prisma client
from models.asset import Asset  # Adjust imports if necessary
from models.transaction import Transaction  # Adjust imports if necessary
from flask import Flask

app = Flask(__name__)

# Initialize Prisma client
prisma = Prisma()

async def initialize_prisma():
    await prisma.connect()

# Use Flask's "before_first_request" to initialize Prisma
@app.before_first_request
def setup():
    import asyncio
    asyncio.run(initialize_prisma())

class Portfolio:
    def __init__(self):
        self.assets = {}  # Dictionary to store current holdings
        self.transactions = []  # Internal transaction tracking

    async def log_transaction(self, transaction: Transaction):
        """Logs a transaction to the database using Prisma."""
        await prisma.transaction.create(
            data={
                "asset_id": transaction.asset_id,
                "type": transaction.type,
                "amount": transaction.amount,
                "price": transaction.price,
            }
        )

    async def add_asset(self, asset_type: str, asset: Asset, quantity: float, price: float):
        # Record the transaction for tracking
        transaction = Transaction(asset_id=asset.id, type="buy", amount=quantity, price=price)
        await self.log_transaction(transaction)

        # Add or update the asset in the in-memory portfolio
        if asset.id in self.assets:
            self.assets[asset.id]['quantity'] += quantity
        else:
            self.assets[asset.id] = {'asset': asset, 'quantity': quantity}

        # Check if asset exists in the database
        existing_asset = await prisma.asset.find_unique(where={"id": asset.id})
        if existing_asset:
            # Update quantity if asset already exists
            await prisma.asset.update(
                where={"id": asset.id},
                data={"quantity": existing_asset.quantity + quantity}
            )
        else:
            # Create new asset if not in the database
            await prisma.asset.create(
                data={
                    "id": asset.id,
                    "name": asset.name,
                    "sector": asset.sector,
                    "price": price,
                    "quantity": quantity
                }
            )

    async def remove_asset(self, asset_type: str, asset_id: str, quantity: float, price: float):
        # Ensure the asset exists and has enough quantity to sell
        if asset_id in self.assets and self.assets[asset_id]['quantity'] >= quantity:
            transaction = Transaction(asset_id=asset_id, type="sell", amount=quantity, price=price)
            await self.log_transaction(transaction)

            # Update or remove the asset in the in-memory portfolio
            self.assets[asset_id]['quantity'] -= quantity
            if self.assets[asset_id]['quantity'] <= 0:
                del self.assets[asset_id]

            # Update the asset in the database
            asset = await prisma.asset.find_unique(where={"id": asset_id})
            if asset:
                new_quantity = asset.quantity - quantity
                if new_quantity > 0:
                    await prisma.asset.update(
                        where={"id": asset_id},
                        data={"quantity": new_quantity}
                    )
                else:
                    await prisma.asset.delete(where={"id": asset_id})
        else:
            raise ValueError("Insufficient quantity to sell.")

    async def get_total_value(self) -> float:
        # Calculate total value based on in-memory assets
        return sum(asset_data['asset'].price * asset_data['quantity'] for asset_data in self.assets.values())

    async def get_allocations(self) -> Dict[str, float]:
        total_value = await self.get_total_value()
        return {asset_id: (asset_data['asset'].price * asset_data['quantity']) / total_value
                for asset_id, asset_data in self.assets.items()} if total_value > 0 else {}

    async def get_transaction_history(self) -> list:
        # Fetch transaction history from the database
        transactions = await prisma.transaction.find_many()
        return [
            {"asset_id": t.asset_id, "type": t.type, "quantity": t.amount, "price": t.price}
            for t in transactions
        ]

# Don’t forget to disconnect Prisma when the app is shutting down.
@app.teardown_appcontext
def close_prisma(exception=None):
    prisma.disconnect()
