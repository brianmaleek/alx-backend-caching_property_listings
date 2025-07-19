from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from utils import invalidate_properties_cache

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver([post_save, post_delete], sender=Property)
def invalidate_cache_on_property_change(sender, instance, **kwargs):
    """
    Signal receiver to invalidate the cache when a Property instance is saved or deleted.
    
    Args:
        sender (Model): The model class that sent the signal.
        instance (Property): The instance of the Property model.
        **kwargs: Additional keyword arguments.
    """
    invalidate_properties_cache()
    print(f"Cache invalidated for property: {instance.title} (ID: {instance.id})")
