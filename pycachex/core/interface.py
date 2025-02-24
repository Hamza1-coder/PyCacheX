from abc import ABC, abstractmethod

class CacheInterface(ABC):
  @abstractmethod
  def get(self, key):
    """Retrieve an item from the cache."""
    pass

  @abstractmethod
  def set(self, key, value, ttl=None):
    """
    Store an item in the cache.
    
    Parameters:
        key: Unique identifier for the cached item.
        value: The data to cache.
        ttl: Optional time-to-live (in seconds) for automatic expiration.
    """
    pass

  @abstractmethod
  def delete(self, key):
    """Remove a specific item from the cache."""
    pass
  
    @abstractmethod
    def clear(self):
        """Clear all items from the cache."""
        pass
