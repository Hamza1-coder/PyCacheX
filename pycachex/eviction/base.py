from abc import ABC, abstractmethod

class EvictionPolicy(ABC):
    @abstractmethod
    def record_access(self, key):
        """Called whenever a key is accessed (e.g., via get())."""
        pass

    @abstractmethod
    def record_insertion(self, key):
        """Called when a key is inserted into the cache."""
        pass

    @abstractmethod
    def evict(self, cache):
        """
        Determine which key should be evicted from the cache.
        
        Parameters:
            cache: The current cache dictionary.
            
        Returns:
            The key to evict.
        """
        pass

    @abstractmethod
    def remove_key(self, key):
        """Remove a key from internal tracking when it is deleted from the cache."""
        pass