from rest_framework import serializers
from vendor.models import Stock
from products.api.serializers import FeatureAttributeSerializer
from django.db.models import Sum, F
from products.api.serializers import ProductsSerializer
from products.models import Product

class StockSerializer(serializers.ModelSerializer):
    attributes = FeatureAttributeSerializer(many=True, read_only=True)
    class Meta:
        model = Stock
        fields = '__all__'

class StockItemSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField('get_product')
    quantity = serializers.IntegerField()

    def get_product(self, obj):
        priduct = Product.objects.get(id=obj['product'])
        serializer = ProductsSerializer(priduct, many=False)
        return serializer.data
