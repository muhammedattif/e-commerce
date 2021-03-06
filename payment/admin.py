from django.contrib import admin
from .models import Cart, CartItem

class CartConfig(admin.ModelAdmin):
    model = Cart

    list_filter = ('user', 'sub_total', 'total', 'discount', 'taxes')
    list_display = ('user', 'sub_total', 'total', 'discount', 'taxes')

    readonly_fields=('sub_total', 'total', 'discount', 'taxes')

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


admin.site.register(CartItem, CartItemConfig)
admin.site.register(Cart, CartConfig)
