from django.urls import path, include
from .views import OrdersListCreateView, OrderRetriveUpdateView, OrderCancellingView
app_name = 'orders'

urlpatterns = [
    path('', OrdersListCreateView.as_view(), name="orders-list"),
    path('<id>/', OrderRetriveUpdateView.as_view(), name="orders-retrive-update"),
    path('<id>/cancel', OrderCancellingView.as_view(), name="order-cancelling"),
  ]
