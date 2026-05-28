"""
Caching module for storing graph invocation results with TTL.
"""
from cachetools import TTLCache

# TTL-based cache using cachetools (60-second TTL, max 1000 entries)
_CACHE = TTLCache(maxsize=1000, ttl=60)


def get(key):
    """Retrieve a value from cache if it exists."""
    return _CACHE.get(key)


def set(key, value):
    """Store a value in cache with automatic TTL expiration."""
    _CACHE[key] = value


def has(key):
    """Check if a key exists in cache."""
    return key in _CACHE


def clear():
    """Clear all cache entries."""
    _CACHE.clear()
