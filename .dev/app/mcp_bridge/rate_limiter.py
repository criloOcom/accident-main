"""Rate limiting module for MCP servers."""

import time
import threading
from collections import deque
from typing import Optional


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, max_calls: int = 10, period: float = 60.0):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds (default: 60 seconds)
        """
        self.max_calls = max_calls
        self.period = period
        self._calls: deque = deque()
        self._lock = threading.RLock()
    
    def wait_if_needed(self) -> float:
        """
        Wait if necessary to respect rate limit.
        
        Returns:
            Time waited in seconds
        """
        with self._lock:
            now = time.time()
            
            # Remove old entries
            while self._calls and self._calls[0] < now - self.period:
                self._calls.popleft()
            
            # Check if we need to wait
            if len(self._calls) >= self.max_calls:
                sleep_time = self._calls[0] + self.period - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    return sleep_time
            
            # Record this call
            self._calls.append(time.time())
            return 0.0
    
    def can_proceed(self) -> bool:
        """Check if a call can proceed without waiting."""
        with self._lock:
            now = time.time()
            
            # Remove old entries
            while self._calls and self._calls[0] < now - self.period:
                self._calls.popleft()
            
            return len(self._calls) < self.max_calls
    
    @property
    def remaining(self) -> int:
        """Get remaining calls in current period."""
        with self._lock:
            now = time.time()
            
            # Remove old entries
            while self._calls and self._calls[0] < now - self.period:
                self._calls.popleft()
            
            return max(0, self.max_calls - len(self._calls))
    
    @property
    def reset_time(self) -> float:
        """Get time until rate limit resets."""
        with self._lock:
            if not self._calls:
                return 0.0
            
            oldest = self._calls[0]
            reset_at = oldest + self.period
            return max(0.0, reset_at - time.time())


# Global rate limiters for different APIs
judilibre_limiter = RateLimiter(max_calls=10, period=60.0)  # 10 calls per minute
legifrance_limiter = RateLimiter(max_calls=10, period=60.0)  # 10 calls per minute
