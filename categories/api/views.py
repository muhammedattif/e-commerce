from categories.models import Category, Brand
from .serializers import CategorySerializer, BrandSerializer
from rest_framework.generics import ListAPIView


class CategoryList(ListAPIView):
    permission_classes = ()
    queryset = Category.objects.prefetch_related('childs').filter(parent=None)
    serializer_class = CategorySerializer

class BrandList(ListAPIView):
    permission_classes = ()
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
