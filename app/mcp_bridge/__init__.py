"""Common utilities for MCP servers."""

from .cache import TTLCache, taxonomy_cache, decision_cache, cached
from .retry import retry_with_backoff, retry_on_error, handle_http_error, RateLimitError, TemporaryServerError
from .rate_limiter import RateLimiter, judilibre_limiter, legifrance_limiter
from .zones import extract_zones, format_zones_for_display, get_zone_summary, format_highlights
from .offline_cache import OfflineCache, offline_cache

__all__ = [
    "TTLCache",
    "taxonomy_cache",
    "decision_cache",
    "cached",
    "retry_with_backoff",
    "retry_on_error",
    "handle_http_error",
    "RateLimitError",
    "TemporaryServerError",
    "RateLimiter",
    "judilibre_limiter",
    "legifrance_limiter",
    "extract_zones",
    "format_zones_for_display",
    "get_zone_summary",
    "format_highlights",
    "OfflineCache",
    "offline_cache"
]
