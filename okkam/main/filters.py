from django_filters import rest_framework as filters
from .models import WebPage

class WebPageFilter(filters.FilterSet):
    """Filter class which allows to filter :model:`main.WebPage` by specific fields."""
    url = filters.CharFilter(lookup_expr='contains')
    ip_address = filters.CharFilter(lookup_expr='contains')
    http_code = filters.NumberFilter()

    class Meta:
        model = WebPage
        fields = {
            'url',
            'ip_address',
            'http_code',
        }