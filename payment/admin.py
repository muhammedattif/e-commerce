from django.contrib import admin
from .models import CartItem


class CartItemConfig(admin.ModelAdmin):
    model = CartItem

    list_filter = ('user', 'product')
    list_display = ('user', 'product')

admin.site.register(CartItem, CartItemConfig)
