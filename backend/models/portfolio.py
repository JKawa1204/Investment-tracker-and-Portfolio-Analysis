# backend/models/portfolio.py
from typing import Dict
from backend.models.asset import Asset

class Portfolio:
    def __init__(self):
        self.assets = {}

    def add_asset(self, asset: Asset, quantity: float):
        if asset.id in self.assets:
            self.assets[asset.id]['quantity'] += quantity
        else:
            self.assets[asset.id] = {'asset': asset, 'quantity': quantity}

    def remove_asset(self, asset_id: str, quantity: float):
        if asset_id in self.assets:
            self.assets[asset_id]['quantity'] -= quantity
            if self.assets[asset_id]['quantity'] <= 0:
                del self.assets[asset_id]

    def get_total_value(self) -> float:
        return sum(asset_data['asset'].price * asset_data['quantity'] for asset_data in self.assets.values())

    def get_allocations(self) -> Dict[str, float]:
        total_value = self.get_total_value()
        allocations = {asset_id: (asset_data['asset'].price * asset_data['quantity']) / total_value
                       for asset_id, asset_data in self.assets.items()}
        return allocations
