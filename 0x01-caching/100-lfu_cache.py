#!/usr/bin/env python3
"""LFUCache caching system."""


from collections import defaultdict, OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache caching system."""

    def __init__(self):
        """LFUCache."""
        super().__init__()
        self.freq = defaultdict(OrderedDict)
        self.min_freq = 0
        self.key_freq = {}

    def _update_freq(self, key):
        """Update Freq of key."""
        freq = self.key_freq[key]
        value = self.cache_data[key]

        del self.freq[freq][key]
        if not self.freq[freq]:
            del self.freq[freq]
            if freq == self.min_freq:
                self.min_freq += 1

        self.freq[freq + 1][key] = value
        self.key_freq[key] = freq + 1

    def put(self, key, value):
        """Put to cache."""
        if not key or not value:
            return None
        if key in self.cache_data:
            self.cache_data[key] = value
            self._update_freq(key)
        else:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                evict_key, _ = self.freq[self.min_freq].popitem(last=False)
                del self.cache_data[evict_key]
                del self.key_freq[evict_key]
                print(f"DISCARD: {evict_key}")

            self.cache_data[key] = value
            self.freq[1][key] = value
            self.key_freq[key] = 1
            self.min_freq = 1

    def get(self, key):
        """Retrive from cache."""
        if key not in self.cache_data:
            return None
        self._update_freq(key)
        return self.cache_data[key]
