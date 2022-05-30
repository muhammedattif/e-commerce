from rest_framework import serializers
from vendor.models import Stock, JoinForm
from products.api.serializers import FeatureOptionSerializer
from django.db.models import Sum, F
from products.api.serializers import ProductsSerializer
from products.models import Product
from django.contrib.auth import get_user_model
from djmoney.contrib.django_rest_framework import MoneyField

User = get_user_model()

class VendorProductUpdateSerializer(serializers.ModelSerializer):
    price = MoneyField(max_digits=10, decimal_places=2)
    discount = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ('id','name', 'description', 'price', 'discount', 'minimum_cart_quantity', 'cover')


class VendorSerlializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'avatar', 'location')

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
        return obj['creation']


class ReportSerializer(serializers.Serializer):
    sales = SalesSerializer(many=True, read_only=True)
    number_of_orders = serializers.IntegerField()
    orders_amount = serializers.DecimalField(max_digits=14, decimal_places=4)
    number_of_items_sold = serializers.IntegerField()
    received_payments = serializers.DecimalField(max_digits=14, decimal_places=4)
    daily_sales = serializers.DecimalField(max_digits=14, decimal_places=4)


class JoinFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinForm
        fields = '__all__'
