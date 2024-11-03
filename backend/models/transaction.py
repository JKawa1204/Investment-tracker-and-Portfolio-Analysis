from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

class Transaction(BaseModel):
    asset_symbol: str
    transaction_type: str
    amount: Decimal
    price: Decimal
    purchase_date: datetime = datetime.now()

    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.transaction_type not in ["buy", "sell"]:
            raise ValueError("Transaction type must be 'buy' or 'sell'")

class TransactionHistory:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.transactions.sort(key=lambda x: x.purchase_date, reverse=True)

    def get_transactions(self, asset_symbol: Optional[str] = None) -> List[Transaction]:
        if asset_symbol:
            return [t for t in self.transactions if t.asset_symbol == asset_symbol]
        return self.transactions

    def get_transactions_by_date_range(self, 
                                       start_date: Optional[datetime] = None,
                                       end_date: Optional[datetime] = None) -> List[Transaction]:
        filtered_transactions = self.transactions
        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t.purchase_date >= start_date]
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t.purchase_date <= end_date]
        return filtered_transactions

    def clear_history(self):
        self.transactions = []