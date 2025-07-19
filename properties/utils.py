from django.core.cache import cache
from .models import Property

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

def invalidate_properties_cache():
    """
    Invalidates the cache for properties.
    This should be called whenever properties are updated or deleted.
    """
    cache.delete('all_properties')
    print("Cache invalidated for all properties.")
