from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Items
from .serializers import ItemsSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['name', 'quantity', 'distance']
    filterset_fields = ['date', 'name', 'quantity', 'distance']
