from django_filters import rest_framework as filters
from .models import Items

class ItemsFilter(filters.FilterSet):
    name_contains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    quantity_gt = filters.NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity_lt = filters.NumberFilter(field_name='quantity', lookup_expr='lt')
    distance_gt = filters.NumberFilter(field_name='distance', lookup_expr='gt')
    distance_lt = filters.NumberFilter(field_name='distance', lookup_expr='lt')

    class Meta:
        model = Items
        fields = []