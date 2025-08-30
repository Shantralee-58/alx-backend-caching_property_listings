from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)  # Optional: still cache the response for 15 minutes
def property_list(request):
    properties = get_all_properties()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': prop.price,
        }
        for prop in properties
    ]
    return JsonResponse({'data': data})

