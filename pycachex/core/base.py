from .interface import CacheInterface
from .exceptions import InvalidKeyError
import time
import threading
import logging

logger = logging.getLogger(__name__)

class BaseCache(CacheInterface):
    def __init__(self, default_ttl=None):
        """
        Initialize the cache.
        
        Parameters:
            default_ttl: Default time-to-live (in seconds) for cached items.
        """
        self.default_ttl = default_ttl
        self._cache = {}  # Internal dictionary: key -> (value, expiry)
        self._lock = threading.Lock()
        logger.info("BaseCache initialized with default TTL: %s", default_ttl)

    def get(self, key):
        """Retrieve an item from the cache if it's valid."""
        try:
            # Validate key (must be hashable)
            hash(key)
        except Exception as e:
            logger.error("Invalid key provided to get(): %s. Error: %s", key, e)
            raise InvalidKeyError(f"Invalid key: {key}") from e

        with self._lock:
            record = self._cache.get(key)
            if record:
                value, expiry = record
                if expiry is None or expiry > time.time():
                    logger.debug("Cache hit for key: %s", key)
                    return value
                else:
                    logger.info("Cache expired for key: %s", key)
                    # The item has expired; remove it.
                    self.delete(key)
            logger.debug("Cache miss for key: %s", key)
            return None

    def set(self, key, value, ttl=None):
        """
        Store an item in the cache with an optional TTL.

        Parameters:
            key: The key under which the value is stored.
            value: The value to store.
            ttl: Time-to-live in seconds; if None, uses default_ttl.
        """
        try:
            hash(key)
        except Exception as e:
            logger.error("Invalid key provided to set(): %s. Error: %s", key, e)
            raise InvalidKeyError(f"Invalid key: {key}") from e

        with self._lock:
            ttl = ttl if ttl is not None else self.default_ttl
            expiry = time.time() + ttl if ttl else None
            self._cache[key] = (value, expiry)
            logger.debug("Set key: %s with ttl: %s", key, ttl)

    def delete(self, key):
        """Remove an item from the cache."""
        try:
            hash(key)
        except Exception as e:
            logger.error("Invalid key provided to delete(): %s. Error: %s", key, e)
            raise InvalidKeyError(f"Invalid key: {key}") from e

        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug("Deleted key: %s from cache", key)
            else:
                logger.warning("Attempted to delete non-existent key: %s", key)

    def clear(self):
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            logger.info("Cache cleared")