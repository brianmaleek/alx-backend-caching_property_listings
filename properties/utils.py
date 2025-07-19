import logging
from django_redis import get_redis_connection
from django.core.cache import cache
from .models import Property

# Setup logging
logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieves the list of properties from the cache or database.
    
    Returns:
        list: A list of Property objects.
    """
    # Check if the property list is cached
    cached_properties = cache.get('property_list')
    
    if cached_properties is not None:
        # If properties are cached, return them directly
        return cached_properties

    # If not cached, fetch from the database and cache the result
    properties = Property.objects.all()

    # Store in Redis cache for 1 hour (3600 Seconds)
    cache.set('all_properties', properties, 3600)  

    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - keyspace_hits: Number of successful cache hits
            - keyspace_misses: Number of cache misses
            - hit_ratio: Calculated hit ratio (hits / (hits + misses))
            - total_requests: Total number of cache requests
            - cache_efficiency: Hit ratio as percentage
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")

        # Get redis INFO command output
        info = redis_conn.info()

        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        # Calculate hit ratio and cache efficiency
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0
        cache_efficiency = hit_ratio * 100  # Convert to percentage

        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'cache_efficiency': round(cache_efficiency, 2),
            'redis_version': info.get('redis_version', 'Unknown'),
            'connected_clients': info.get('connected_clients', 0),
            'used_memory_human': info.get('used_memory_human', 'Unknown'),
            'uptime_in_seconds': info.get('uptime_in_seconds', 0),
        }
        # Log the metrics
        logger.info(f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
                f"Hit Ratio: {cache_efficiency:.2f}%, Total Requests: {total_requests}")
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
            'cache_efficiency': 0,
        }
