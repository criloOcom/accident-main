"""Retry module with exponential backoff for MCP servers."""

import time
import random
import logging
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    """Exception raised when API rate limit is exceeded (HTTP 429)."""
    pass


class ServerError(Exception):
    """Exception raised when server returns an error (HTTP 5xx)."""
    pass


class TemporaryServerError(Exception):
    """Exception raised for temporary server errors (HTTP 429, 502, 503, 504)."""
    pass


def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    retryable_exceptions: tuple = (RateLimitError, TemporaryServerError)
) -> Any:
    """
    Execute function with retry and exponential backoff.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Add random jitter to delay
        retryable_exceptions: Exceptions that trigger retry
    
    Returns:
        Function result
    
    Raises:
        Last exception if all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except retryable_exceptions as e:
            last_exception = e
            
            if attempt == max_retries:
                break
            
            # Calculate delay with exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            # Add jitter if enabled
            if jitter:
                delay = delay * (0.5 + random.random())
            
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )
            time.sleep(delay)
    
    raise last_exception


def retry_on_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
):
    """
    Decorator to retry function on error with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Add random jitter to delay
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, TemporaryServerError) as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    
                    # Add jitter if enabled
                    if jitter:
                        delay = delay * (0.5 + random.random())
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
            
            raise last_exception
        return wrapper
    return decorator


def handle_http_error(status_code: int, response_text: str = "") -> None:
    """
    Handle HTTP errors and raise appropriate exceptions.
    
    Args:
        status_code: HTTP status code
        response_text: Response body text
    
    Raises:
        RateLimitError for 429
        TemporaryServerError for 502, 503, 504
        ServerError for other 5xx errors
    """
    if status_code == 429:
        raise RateLimitError(f"Rate limit exceeded: {response_text}")
    elif status_code in (502, 503, 504):
        raise TemporaryServerError(f"Server temporarily unavailable ({status_code}): {response_text}")
    elif 500 <= status_code < 600:
        raise ServerError(f"Server error ({status_code}): {response_text}")
