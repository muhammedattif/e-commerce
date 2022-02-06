from rest_framework import serializers
from vendor.models import Stock
from products.api.serializers import FeatureOptionSerializer
from django.db.models import Sum, F
from products.api.serializers import ProductsSerializer
from products.models import Product

class StockSerializer(serializers.ModelSerializer):
    options = FeatureOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Stock
        fields = '__all__'

class StockItemSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField('get_quantity')
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity')

    def get_quantity(self, product):
        return product.quantity
