from django.urls import path, include
from .views import OrdersListView
app_name = 'orders'

urlpatterns = [
    path('', OrdersListView.as_view(), name="orders-list"),
  ]
