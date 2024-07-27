#!/usr/bin/env python3
"""FIFOCache caching system."""


BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache caching system."""

    def __init__(self):
        """FIFOCache."""
        super().__init__()

    def put(self, key, item):
        """Put to cache."""
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS and \
                 key not in self.cache_data.keys():
                x = next(iter(self.cache_data.keys()))
                self.cache_data.pop(x)
                print(f'DISCARD: {x}')

            self.cache_data[key] = item

    def get(self, key):
        """Retrive from cache."""
        if key:
            try:
                return self.cache_data[key]
            except Exception as e:
                pass
        return None
