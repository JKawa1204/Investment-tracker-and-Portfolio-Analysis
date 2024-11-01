from config.symbols import get_stock_symbols, get_symbol_name

class Transaction:
    def __init__(self, asset_id: str, type: str, amount: float):
        self.asset_id = asset_id
        self.type = type  # "buy" or "sell"
        self.amount = amount
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

    def display_transactions(self):
        current = self.head
        while current:
            print(f"Transaction: {current.type} {current.amount} of {current.asset_id}")
            current = current.next
