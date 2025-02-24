from collections import OrderedDict
from .base import EvictionPolicy

class LRUCachePolicy(EvictionPolicy):
    def __init__(self):
        # OrderedDict to keep track of key usage order.
        self.order = OrderedDict()

    def record_access(self, key):
        # Update the order by moving the key to the end.
        if key in self.order:
            self.order.move_to_end(key)
        else:
            self.order[key] = True

    def record_insertion(self, key):
        # Insert the key and move it to the end.
        self.order[key] = True
        self.order.move_to_end(key)

    def evict(self, cache):
        # Evict the least recently used key (first item in the order).
        if self.order:
            oldest_key, _ = self.order.popitem(last=False)
            return oldest_key
        return None

    def remove_key(self, key):
        # Remove the key from our tracking.
        if key in self.order:
            del self.order[key]