# backend/algorithms/diversification.py
from collections import defaultdict
from typing import List, Dict

class Diversification:
    def __init__(self, assets: List[Dict[str, str]]):
        self.assets = assets  # Each asset has fields like "id" and "sector"

    def check_diversification(self) -> Dict[str, float]:
        sector_count = defaultdict(int)
        total_assets = len(self.assets)

        for asset in self.assets:
            sector_count[asset['sector']] += 1

        # Calculate sector concentration as a percentage
        concentration = {sector: count / total_assets for sector, count in sector_count.items()}

        return concentration  # Returns a dictionary with sector concentration percentages
