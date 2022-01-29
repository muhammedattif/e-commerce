from rest_framework.generics import ListAPIView
from products.models import Product, Review
from products.api.serializers import ReviewSerializer, VendorProductsSerializer, VendorReviewsSerializer

class VendorProductList(ListAPIView):
    serializer_class = VendorProductsSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand', 'vendor'
        ).prefetch_related('features__attributes', 'category__childs', 'images', 'reviews'
        ).filter(vendor=self.request.user)
        return queryset


class VendorProductReviewsList(ListAPIView):
    serializer_class = VendorReviewsSerializer

    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product').filter(product__vendor=self.request.user)
        return queryset
