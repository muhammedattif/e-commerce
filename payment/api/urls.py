from django.urls import path, include
from .views import BaseListCreateCartItemView, CartItemView, CheckoutView
app_name = 'payment'

urlpatterns = [
    path('cart/', BaseListCreateCartItemView.as_view(), name="cart"),
    path('cart/items/<int:id>/', CartItemView.as_view(), name="cart-item"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
  ]
