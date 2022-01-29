from django.urls import path, include
from .views import BaseListCreateCartItemView, CheckoutView
app_name = 'payment'

urlpatterns = [
    path('cart/', BaseListCreateCartItemView.as_view(), name="cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
  ]
