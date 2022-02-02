from django.contrib import admin
from .models import Stock


class StockConfig(admin.ModelAdmin):
    model = Stock

    list_filter = ('product', 'quantity')
    list_display = ('product', 'quantity')

    fields = ('product', 'attributes', 'quantity')

    def get_queryset(self, request):
        queryset = super(StockConfig, self).get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('attributes__feature')
        return queryset

admin.site.register(Stock, StockConfig)
