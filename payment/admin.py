from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartConfig(admin.ModelAdmin):
    model = Cart

    list_filter = ('user', 'sub_total', 'total', 'discount', 'taxes')
    list_display = ('user', 'sub_total', 'total', 'discount', 'taxes')

    readonly_fields=('user', 'sub_total', 'total', 'discount', 'taxes')

    def get_queryset(self, request):
        queryset = super(CartConfig, self).get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset

class CartItemConfig(admin.ModelAdmin):
    model = CartItem

    list_filter = ('product', 'cart', 'stock', 'quantity')
    list_display = ('product', 'cart', 'stock', 'quantity')

    readonly_fields=('quantity', )

    def get_queryset(self, request):
        queryset = super(CartItemConfig, self).get_queryset(request)
        queryset = queryset.select_related('product', 'cart__user', 'stock__product')
        return queryset

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

admin.site.register(CartItem, CartItemConfig)
admin.site.register(Cart, CartConfig)
admin.site.register(Order, OrderConfig)
admin.site.register(OrderItem)
