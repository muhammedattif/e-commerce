from django.urls import path, include
from .views import (
BaseListCreateProductView,
ProductDetail,
ProductAvailability,
ReviewsListCreateView,
CheckReview,
ProductFilter,
OffersListView,
BestSellerListView
)

app_name = 'products'

urlpatterns = [
    path('', BaseListCreateProductView.as_view(), name="products"),
    path('offers/', OffersListView.as_view(), name="offers"),
    path('best-seller/', BestSellerListView.as_view(), name="best-seller"),
    path('filter/', ProductFilter.as_view(), name="filter"),
    path('<int:id>/', ProductDetail.as_view(), name="product_detail"),
    path('<int:id>/check', ProductAvailability.as_view(), name="product_check"),
    path('<int:id>/reviews', ReviewsListCreateView.as_view(), name="product_reviews"),
    path('<int:id>/reviews/check', CheckReview.as_view(), name="check_review")
  ]
