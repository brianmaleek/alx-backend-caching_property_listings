from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
def invalidate_cache_on_property_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a property is created or updated.
    
    Args:
        sender (Model): The model class that sent the signal.
        instance (Property): The instance of the Property that was saved.
        created: Boolean indicating if the instance was created or updated.
        **kwargs: Additional keyword arguments.
    """
    cache.delete('all_properties')
    print(f"Cache invalidated: Property {'created' if created  else 'updated'}")

@receiver(post_delete, sender=Property)
def clear_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a property is deleted.
    
    Args:
        sender (Model): The model class that sent the signal.
        instance (Property): The instance of the Property that was deleted.
        **kwargs: Additional keyword arguments.
    """
    cache.delete('all_properties')
    print(f"Cache cleared for Property with id {instance.id} on delete.")
