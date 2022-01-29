from rest_framework.generics import ListAPIView
from products.models import Product
from vendor.api.serializers import VendorProductSerializer

class VendorProductList(ListAPIView):
    queryset = Product.objects.filter(vendor=request.user)
    serializer_class = VendorProductSerializer
