#!/usr/bin/env python3
"""MRUCache caching system."""


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRUCache caching system."""

    def __init__(self):
        """MRUCache."""
        super().__init__()

    def put(self, key, item):
        """Put to cache."""
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS and \
                 key not in self.cache_data.keys():
                most_recent_key = next(reversed(self.cache_data))
                self.cache_data.pop(most_recent_key)
                print(f'DISCARD: {most_recent_key}')

            self.cache_data[key] = item

    def get(self, key):
        """Retrive from cache."""
        if key:
            try:
                value = self.cache_data.pop(key)
                self.cache_data[key] = value
                return value
            except Exception as e:
                pass
        return None
