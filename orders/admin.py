from django.contrib import admin
from .models import Order, OrderItem


class OrderConfig(admin.ModelAdmin):
    model = Order

    list_filter = (
    'user',
    'address',
    'sub_total',
    'total',
    'discount',
    'taxes',
    'is_processed',
    'is_shipped',
    'is_in_route',
    'is_arrived',
    'is_paid',
    'is_cancelled'
    )
    list_display = (
    'user',
    'address',
    'sub_total',
    'total',
    'discount',
    'taxes',
    'is_paid',
    'is_cancelled'
    )
    fields = (
    'user',
    'address',
    'sub_total',
    'total',
    'discount',
    'taxes',
    'is_processed',
    'is_shipped',
    'is_in_route',
    'is_arrived',
    'is_paid',
    'is_cancelled'
    )
    search_fields = ('items__product__name', 'items__product__description')
    readonly_fields = ('user', 'address', 'sub_total', 'total', 'discount', 'taxes')
    list_select_related = ('user', 'address__user')
    ordering = ['creation']

    def get_queryset(self, request):
        queryset = super(OrderConfig, self).get_queryset(request)
        queryset = queryset.select_related('user', 'address').prefetch_related('address__user')
        return queryset

class OrderItemConfig(admin.ModelAdmin):
    model = OrderItem

    list_display = ('product', 'order', 'stock', 'quantity')
    fields = ('product', 'order', 'stock', 'quantity')

    search_fields = ('product__name', 'product__description')

admin.site.register(Order, OrderConfig)
admin.site.register(OrderItem, OrderItemConfig)
