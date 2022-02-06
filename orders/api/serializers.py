from rest_framework import serializers
from products.api.serializers import CartProductSerializer
from vendor.api.serializers import StockSerializer
from orders.models import Order, OrderItem


class VendorOrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(many=False, read_only=True)
    stock = StockSerializer(many=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField('get_discount_percentage')
    class Meta:
        model = Order
        fields = ('id', 'total', 'total_currency', 'sub_total', 'sub_total_currency', 'discount', 'discount_currency', 'discount_percentage' ,  'taxes', 'taxes_currency', 'address')
        depth = 1

    def get_discount_percentage(self, order):
        return (order.discount/order.sub_total)*100
