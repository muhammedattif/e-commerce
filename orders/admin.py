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

    readonly_fields=('user', 'address', 'sub_total', 'total', 'discount', 'taxes')

    def get_queryset(self, request):
        queryset = super(OrderConfig, self).get_queryset(request)
        queryset = queryset.select_related('user', 'address').prefetch_related('address__user')
        return queryset
        
admin.site.register(Order, OrderConfig)
admin.site.register(OrderItem)
