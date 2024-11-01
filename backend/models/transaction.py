# backend/models/transaction.py

class Transaction:
    def __init__(self, asset_id: str, type: str, amount: float, price: float):
        self.asset_id = asset_id
        self.type = type  # "buy" or "sell"
        self.amount = amount
        self.price = price  # Price at the time of transaction
        self.next = None
        self.prev = None

class TransactionHistory:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_transaction(self, transaction: Transaction):
        if not self.head:
            self.head = self.tail = transaction
        else:
            self.tail.next = transaction
            transaction.prev = self.tail
            self.tail = transaction

    def get_transactions(self, asset_id: str):
        transactions = []
        current = self.head
        while current:
            if current.asset_id == asset_id:
                transactions.append(current)
            current = current.next
        return transactions
