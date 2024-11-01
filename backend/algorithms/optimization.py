# backend/algorithms/optimization.py
from typing import Dict

class Optimization:
    def __init__(self, current_allocations: Dict[str, float], target_allocations: Dict[str, float]):
        self.current_allocations = current_allocations
        self.target_allocations = target_allocations

    def rebalance(self) -> Dict[str, float]:
        adjustments = {}

        for asset_id, target_weight in self.target_allocations.items():
            current_weight = self.current_allocations.get(asset_id, 0)
            adjustments[asset_id] = target_weight - current_weight

        return adjustments  # Returns a dictionary of assets and their necessary weight adjustments
