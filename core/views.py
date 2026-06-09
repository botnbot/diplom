from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from .models import Items
from .serializers import ItemsSerializer
from .filters import ItemsFilter   # важно!

class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemsFilter
    ordering_fields = ['name', 'quantity', 'distance']