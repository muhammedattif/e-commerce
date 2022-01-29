from django.urls import path, include
from .views import BaseListCreateProductView, ProductDetail, ReviewsListCreateView, CheckReview, ProductFilter
app_name = 'products'

urlpatterns = [
    path('', BaseListCreateProductView.as_view(), name="products"),
    path('filter/', ProductFilter.as_view(), name="filter"),
    path('<int:id>/', ProductDetail.as_view(), name="product_detail"),
    path('<int:id>/reviews', ReviewsListCreateView.as_view(), name="product_reviews"),
    path('<int:id>/reviews/check', CheckReview.as_view(), name="check_review")
  ]
