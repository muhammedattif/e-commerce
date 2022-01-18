from django.urls import path, include
from .views import BaseListCreateCartItemView
app_name = 'payment'

urlpatterns = [
    path('cart', BaseListCreateCartItemView.as_view(), name="cart"),
  ]
