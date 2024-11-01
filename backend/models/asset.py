# backend/models/asset.py
class Asset:
    def __init__(self, id: str, name: str, sector: str, price: float):
        self.id = id
        self.name = name
        self.sector = sector
        self.price = price
