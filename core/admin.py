from django.contrib import admin
from .models import Items

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'date', 'distance')
    list_filter = ('name', 'date')
    search_fields = ('name',)
    list_editable = ('name', 'quantity', 'distance')
    fields = ('date', 'name', 'quantity', 'distance')  # ← id УБРАТЬ!
    ordering = ('-date',)
    list_per_page = 10