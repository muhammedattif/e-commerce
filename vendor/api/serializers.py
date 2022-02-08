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


class SalesSerializer(serializers.Serializer):
    day = serializers.SerializerMethodField('get_day')
    total = serializers.DecimalField(max_digits=14, decimal_places=4)

    def get_day(self, obj):
        print(obj)
        return obj['creation__date']


class ReportSerializer(serializers.Serializer):
    sales = SalesSerializer(many=True, read_only=True)
    number_of_orders = serializers.IntegerField()
    orders_amount = serializers.DecimalField(max_digits=14, decimal_places=4)
    number_of_items_sold = serializers.IntegerField()
    received_payments = serializers.DecimalField(max_digits=14, decimal_places=4)
    daily_sales = serializers.DecimalField(max_digits=14, decimal_places=4)
