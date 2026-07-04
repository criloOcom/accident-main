"""Cache module for MCP servers with TTL support."""

import time
import threading
from typing import Any, Optional
from functools import wraps


class TTLCache:
    """Thread-safe cache with Time-To-Live expiration."""
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self._cache: dict[str, dict] = {}
        self._lock = threading.RLock()
        self._default_ttl = default_ttl
        self._stats = {"hits": 0, "misses": 0}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry["expires_at"]:
                    self._stats["hits"] += 1
                    return entry["value"]
                else:
                    del self._cache[key]
            self._stats["misses"] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional custom TTL."""
        with self._lock:
            ttl_seconds = ttl or self._default_ttl
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl_seconds,
                "created_at": time.time()
            }
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def get_or_set(self, key: str, factory, ttl: Optional[int] = None) -> Any:
        """Get value from cache or compute and store it."""
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value
    
    @property
    def stats(self) -> dict:
        """Return cache statistics."""
        return {
            "size": len(self._cache),
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": (
                self._stats["hits"] / (self._stats["hits"] + self._stats["misses"])
                if (self._stats["hits"] + self._stats["misses"]) > 0
                else 0
            )
        }
    
    def cleanup(self) -> None:
        """Remove expired entries."""
        with self._lock:
            now = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if now >= entry["expires_at"]
            ]
            for key in expired_keys:
                del self._cache[key]


# Global cache instance for taxonomies
taxonomy_cache = TTLCache(default_ttl=3600)  # 1 hour

# Global cache instance for decisions
decision_cache = TTLCache(default_ttl=86400)  # 24 hours


def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]
            key_parts.extend(str(a) for a in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            result = taxonomy_cache.get(cache_key)
            if result is not None:
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            taxonomy_cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
