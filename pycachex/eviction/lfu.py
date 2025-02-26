from .base import EvictionPolicy

class LFUCachePolicy(EvictionPolicy):
    def __init__(self):
        # Dictionary to track the access count for each key.
        self.freq = {}

    def record_access(self, key):
        # Increment the usage count on each access.
        if key in self.freq:
            self.freq[key] += 1
        else:
            self.freq[key] = 1

    def record_insertion(self, key):
        # When a key is inserted, initialize its count to 1.
        self.freq[key] = 1

    def evict(self, cache):
        # Determine the key with the lowest frequency.
        if not self.freq:
            return None

        # Find key with minimum frequency.
        min_key = None
        min_count = None
        for key, count in self.freq.items():
            if min_count is None or count < min_count:
                min_count = count
                min_key = key

        # Remove the key from tracking and return it.
        if min_key is not None:
            del self.freq[min_key]
        return min_key

    def remove_key(self, key):
        # Remove the key from tracking if it exists.
        if key in self.freq:
            del self.freq[key]