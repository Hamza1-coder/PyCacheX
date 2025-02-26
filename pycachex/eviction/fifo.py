from collections import deque
from .base import EvictionPolicy

class FIFOCachePolicy(EvictionPolicy):
    def __init__(self):
        # Deque to track insertion order.
        self.order = deque()

    def record_access(self, key):
        # FIFO doesn't change order on access.
        pass

    def record_insertion(self, key):
        # Append key to the end of the queue.
        self.order.append(key)

    def evict(self, cache):
        # Evict the oldest inserted key (from the left of the deque).
        if self.order:
            return self.order.popleft()
        return None

    def remove_key(self, key):
        # Remove the key from the deque if it exists.
        try:
            self.order.remove(key)
        except ValueError:
            # Key not found in order tracking.
            pass
