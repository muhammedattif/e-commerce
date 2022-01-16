from django.urls import path, include
from .views import BaseListCreateProductView, ProductDetail
app_name = 'products'

urlpatterns = [
    path('', BaseListCreateProductView.as_view(), name="products"),
    path('<int:id>/', ProductDetail.as_view(), name="product_detail")
  ]
