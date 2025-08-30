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
    # Try to get the queryset from Redis cache
    properties = cache.get('all_properties')

    if properties is None:
        # Cache miss — fetch from database
        properties = Property.objects.all()
        # Store queryset in cache for 1 hour (3600 seconds)
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
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0

    logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")
    
    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }

