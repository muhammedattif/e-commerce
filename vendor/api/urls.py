from django.urls import path
from .views import VendorProductList
app_name = 'vendor'

urlpatterns = [
    path('products/', VendorProductList.as_view(), name='vendor-products'),
  ]
