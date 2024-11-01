# backend/utils/priority_queue.py
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, priority: float, item):
        heapq.heappush(self.heap, (-priority, item))  # Higher priority comes first

    def pop(self):
        return heapq.heappop(self.heap)[1] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0
