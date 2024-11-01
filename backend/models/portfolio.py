# backend/models/portfolio.py

import os
import csv
from typing import Dict, List
from datetime import datetime
from models.asset import Asset
from models.transaction import Transaction

TRANSACTION_PATH = os.path.join(os.path.dirname(__file__), '../data/transactions.csv')

class Portfolio:
    def __init__(self):
        self.assets = {}  # Dictionary to store current holdings
        self.transactions = []  # Internal transaction tracking

    def log_transaction(self, transaction: Transaction):
        """Logs a transaction to the CSV file."""
        with open(TRANSACTION_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Write headers if file is new
                writer.writerow(['Date', 'Asset ID', 'Type', 'Quantity', 'Price'])
            writer.writerow([datetime.now(), transaction.asset_id, transaction.type, transaction.amount, transaction.price])

    def add_asset(self, asset_type: str, asset: Asset, quantity: float, price: float):
        # Record the transaction for tracking
        transaction = Transaction(asset.id, "buy", quantity, price)
        self.transactions.append(transaction)
        self.log_transaction(transaction)

        # Add or update the asset in the portfolio
        if asset.id in self.assets:
            self.assets[asset.id]['quantity'] += quantity
        else:
            self.assets[asset.id] = {'asset': asset, 'quantity': quantity}

    def remove_asset(self, asset_type: str, asset_id: str, quantity: float, price: float):
        # Ensure the asset exists and has enough quantity to sell
        if asset_id in self.assets and self.assets[asset_id]['quantity'] >= quantity:
            transaction = Transaction(asset_id, "sell", quantity, price)
            self.transactions.append(transaction)
            self.log_transaction(transaction)

            # Update or remove the asset in the portfolio
            self.assets[asset_id]['quantity'] -= quantity
            if self.assets[asset_id]['quantity'] <= 0:
                del self.assets[asset_id]
        else:
            raise ValueError("Insufficient quantity to sell.")

    def get_total_value(self) -> float:
        return sum(asset_data['asset'].price * asset_data['quantity'] for asset_data in self.assets.values())

    def get_allocations(self) -> Dict[str, float]:
        total_value = self.get_total_value()
        return {asset_id: (asset_data['asset'].price * asset_data['quantity']) / total_value
                for asset_id, asset_data in self.assets.items()} if total_value > 0 else {}

    def get_transaction_history(self) -> List[Dict[str, str]]:
        return [
            {"asset_id": t.asset_id, "type": t.type, "quantity": t.amount, "price": t.price}
            for t in self.transactions
        ]
