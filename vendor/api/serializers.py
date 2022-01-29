from rest_framework import serializers
from products.models import Product

class VendorProductSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount', 'quantity', 'features', 'category', 'brand', 'images')
