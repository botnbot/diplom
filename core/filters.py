from django_filters import rest_framework as filters
from .models import Items

class ItemsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='exact')
    name_contains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    quantity_gte = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_gt = filters.NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity_lt = filters.NumberFilter(field_name='quantity', lookup_expr='lt')
    distance_gt = filters.NumberFilter(field_name='distance', lookup_expr='gt')
    distance_lt = filters.NumberFilter(field_name='distance', lookup_expr='lt')

    class Meta:
        model = Items
        fields = []