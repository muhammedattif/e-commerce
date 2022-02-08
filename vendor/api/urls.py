from django.urls import path
from .views import (
VendorProductList,
VendorProductDetail,
VendorProductReviewsList,
VendorOrderList,
StockAPIView,
StockCreateListRetriveAPIView,
ProductStockFeaturesAPIView,
Report
)

app_name = 'vendor'

urlpatterns = [
    path('products/', VendorProductList.as_view(), name='vendor-products'),
    path('products/<int:id>/', VendorProductDetail.as_view(), name='vendor-product'),
    path('reviews/', VendorProductReviewsList.as_view(), name='vendor-products-reviews'),
    path('orders/', VendorOrderList.as_view(), name='vendor-orders'),
    path('stock/', StockAPIView.as_view(), name='vendor-stock'), # All products that has stock
    path('stock/products/<int:id>/', StockCreateListRetriveAPIView.as_view(), name='vendor-stock-create'), # Stocks for this product, Add Stock, Update Stock
    path('stock/products/<int:id>/features/', ProductStockFeaturesAPIView.as_view(), name='vendor-product-stock-features'),
    path('reports/', Report.as_view(), name='reports')
  ]
