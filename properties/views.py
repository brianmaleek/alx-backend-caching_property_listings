from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties

# Create your views here.
@cache_page(60 * 15) #cache for 15 minutes (60 seconds * 15 minutes)
def property_list(request):
    """
    View to list all properties

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        JsonResponse: JSON response containing the list of properties
    """
    properties = get_all_properties()
    
    #convert the properties to a list of dictionaries
    property_data = []
    for property in properties:
        property_data.append({
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),
            'location': property.location,
            'created_at': property.created_at.isoformat(),
        })
    return JsonResponse({
        'properties': property_data,
        'count': len(property_data)
    })
