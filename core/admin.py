from django.contrib import admin
from .models import Items

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'date', 'distance')
    list_filter = ('name', 'quantity', 'date', 'distance')
    search_fields = ('name', )
    list_editable = ('name', 'quantity', 'distance')
    fields = ('id', 'date', 'name', 'quantity', 'distance')
    ordering = ('-date', )
    list_per_page = 10