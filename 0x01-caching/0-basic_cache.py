#!/usr/bin/env python3
"""Basic caching system."""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Basic caching system."""

    def put(self, key, item):
        """Put to cache."""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Retrive from cache."""
        if key:
            try:
                return self.cache_data[key]
            except Exception as e:
                pass
        return None
