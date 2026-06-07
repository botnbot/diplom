from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Items
from .serializers import ItemsSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с Items.
    Поддерживает CRUD операции, фильтрацию, сортировку и пагинацию.
    """
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'quantity', 'distance']
    filterset_fields = ['date', 'name', 'quantity', 'distance']
