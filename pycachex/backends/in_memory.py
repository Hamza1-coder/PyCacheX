from pycachex.core.base import BaseCache
import logging

logger = logging.getLogger(__name__)

class InMemoryCache(BaseCache):
    def __init__(self, default_ttl=None, max_size=None, eviction_policy=None):
        """
        Initialize the in-memory cache.
        
        Parameters:
            default_ttl: Default time-to-live (in seconds) for cached items.
            max_size: Maximum number of items allowed in the cache. If None, the cache is unlimited.
            eviction_policy: Instance of an eviction policy (e.g., LRUCachePolicy).
        """
        super().__init__(default_ttl)
        self.max_size = max_size
        self.eviction_policy = eviction_policy
        logger.info("InMemoryCache initialized with default TTL: %s, max_size: %s, eviction_policy: %s",
                    default_ttl, max_size, eviction_policy)

    def set(self, key, value, ttl=None):
        # Use the BaseCache set() to store the value.
        super().set(key, value, ttl)
        
        # Record insertion event in the eviction policy.
        if self.eviction_policy:
            self.eviction_policy.record_insertion(key)
        
        # If max_size is set and exceeded, evict keys as needed.
        if self.max_size is not None and len(self._cache) > self.max_size:
            if self.eviction_policy:
                evict_key = self.eviction_policy.evict(self._cache)
                if evict_key is not None:
                    super().delete(evict_key)
                    logger.info("Evicted key: %s due to cache size limit", evict_key)

    def get(self, key):
        value = super().get(key)
        if value is not None and self.eviction_policy:
            self.eviction_policy.record_access(key)
        return value

    def delete(self, key):
        if self.eviction_policy:
            self.eviction_policy.remove_key(key)
        super().delete(key)