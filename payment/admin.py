from django.contrib import admin
from .models import CartItem, Order, Cart


admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
