from .base import EvictionPolicy
import time

class TimeBasedCachePolicy(EvictionPolicy):
    def __init__(self):
        # No additional state needed for time-based eviction.
        pass

    def record_access(self, key):
        # No tracking is needed on access for time-based eviction.
        pass

    def record_insertion(self, key):
        # No tracking is needed on insertion; TTL is stored within BaseCache.
        pass

    def evict(self, cache):
        """
        Evict the first key found whose TTL has expired.
        The cache is a dictionary mapping keys to (value, expiry) tuples.
        """
        now = time.time()
        for key, (_, expiry) in cache.items():
            if expiry is not None and expiry < now:
                return key
        # If no expired key is found, return None.
        return None

    def remove_key(self, key):
        # No internal tracking to update.
        pass
