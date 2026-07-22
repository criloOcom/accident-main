"""Offline cache module for MCP servers."""

import json
import os
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OfflineCache:
    """Local cache for decisions and data."""
    
    def __init__(self, cache_dir: str = None):
        """
        Initialize offline cache.
        
        Args:
            cache_dir: Cache directory path (default: ~/.cache/judilibre)
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/judilibre")
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_filepath(self, key: str) -> str:
        """Get filepath for a cache key."""
        # Sanitize key for filesystem
        safe_key = key.replace("/", "_").replace(":", "_")
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def save(self, key: str, data: dict, ttl: int = 86400) -> bool:
        """
        Save data to local cache.
        
        Args:
            key: Cache key
            data: Data to cache
            ttl: Time-to-live in seconds (default: 24 hours)
        
        Returns:
            True if saved successfully
        """
        try:
            filepath = self._get_filepath(key)
            cache_entry = {
                "data": data,
                "timestamp": time.time(),
                "ttl": ttl
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(cache_entry, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
            return False
    
    def load(self, key: str) -> Optional[dict]:
        """
        Load data from local cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached data or None if not found/expired
        """
        try:
            filepath = self._get_filepath(key)
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, "r", encoding="utf-8") as f:
                cache_entry = json.load(f)
            
            # Check if expired
            timestamp = cache_entry.get("timestamp", 0)
            ttl = cache_entry.get("ttl", 86400)
            if time.time() - timestamp > ttl:
                os.remove(filepath)
                return None
            
            return cache_entry.get("data")
        except Exception as e:
            logger.error(f"Error loading from cache: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete data from local cache.
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted successfully
        """
        try:
            filepath = self._get_filepath(key)
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear(self) -> int:
        """
        Clear all cached data.
        
        Returns:
            Number of files deleted
        """
        count = 0
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            if filepath.endswith(".json"):
                try:
                    os.remove(filepath)
                    count += 1
                except Exception as e:
                    logger.error(f"Error deleting {filepath}: {e}")
        return count
    
    def stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_files = 0
        total_size = 0
        expired_files = 0
        
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            if filepath.endswith(".json"):
                total_files += 1
                total_size += os.path.getsize(filepath)
                
                # Check if expired
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        cache_entry = json.load(f)
                    timestamp = cache_entry.get("timestamp", 0)
                    ttl = cache_entry.get("ttl", 86400)
                    if time.time() - timestamp > ttl:
                        expired_files += 1
                except Exception as e:
                    logger.warning(f"Error reading cache file {filepath} for stats: {e}")
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "expired_files": expired_files,
            "cache_dir": self.cache_dir
        }


# Global offline cache instance
offline_cache = OfflineCache()
