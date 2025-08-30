from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all Property objects from Redis cache if available;
    otherwise, fetch from DB and cache for 1 hour.
    """
    properties = cache.get('all_properties')

    if properties is None:
        # Cache miss — fetch from database
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
        logger.info("Cache miss: fetched properties from DB and cached.")
    else:
        logger.info("Cache hit: retrieved properties from Redis cache.")

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Returns a dictionary with hits, misses, and hit_ratio.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses

    # Calculate hit_ratio without using ternary
    hit_ratio = 0
    if total_requests:
        hit_ratio = hits / total_requests

    logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }

