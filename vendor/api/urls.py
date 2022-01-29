from django.urls import path
from .views import VendorProductList, VendorProductReviewsList
app_name = 'vendor'

urlpatterns = [
    path('products/', VendorProductList.as_view(), name='vendor-products'),
    path('reviews/', VendorProductReviewsList.as_view(), name='vendor-products-reviews')
  ]
