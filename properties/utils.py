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
    Retrieve Redis cache metrics and calculate hit ratio.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        # Avoid inline ternary
        if total_requests > 0:
            hit_ratio = hits / total_requests
        else:
            hit_ratio = 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0,
        }

def calculate_hit_ratio(hits, total_requests):
    """
    Calculates and returns hit_ratio.

    Args:
        hits (int): Number of cache hits
        total_requests (int): Total number of requests

    Returns:
        float: The hit ratio (between 0 and 1)
    """
    try:
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        logger.info(f"Calculated hit ratio: {hit_ratio}")
        return hit_ratio
    except Exception as e:
        logger.error(f"Error calculating hit ratio: {e}")
        return 0
