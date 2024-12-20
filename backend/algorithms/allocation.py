import heapq
from typing import List, Dict
class Allocation:
    def __init__(self):
        self.assets = []  # Initialize empty list

    def set_assets(self, assets: List[Dict[str, float]]):
        self.assets = assets
        return self

    def calculate_allocation(self) -> Dict[str, float]:
        if not self.assets:
            return {}
            
        # Use a max-heap (inverted priorities) for allocation based on priority
        heap = [(-asset['priority'], asset['id']) for asset in self.assets]
        heapq.heapify(heap)

        allocation = {}
        total_priority = sum(-priority for priority, _ in heap)

        while heap:
            priority, asset_id = heapq.heappop(heap)
            allocation[asset_id] = -priority / total_priority  # Fractional allocation

        return allocation