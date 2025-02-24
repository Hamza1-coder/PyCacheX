class CacheError(Exception):
    """Base exception class for cache-related errors."""
    pass

class InvalidKeyError(CacheError):
    """Raised when an invalid key is provided to the cache."""
    pass