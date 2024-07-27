#!/usr/bin/env python3
"""LIFOCache caching system."""


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache caching system."""

    def __init__(self):
        """LIFOCache."""
        super().__init__()
        self.lastItem = 0

    def put(self, key, item):
        """Put to cache."""
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                if key not in self.cache_data.keys():
                    self.cache_data.pop(self.lastItem)
                    print(f'DISCARD: {self.lastItem}')

            self.cache_data[key] = item
            self.lastItem = key

    def get(self, key):
        """Retrive from cache."""
        if key:
            try:
                return self.cache_data[key]
            except Exception as e:
                pass
        return None
