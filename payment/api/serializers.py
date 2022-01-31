from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from users.api.serializers import UserBasicInfoSerializer
from products.api.serializers import ProductsSerializer, FeatureAttributesMapSerializer
from payment.models import Cart, CartItem, Order

UserModel = settings.AUTH_USER_MODEL


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=False, read_only=True)
    attributes_map = FeatureAttributesMapSerializer(many=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemCreateSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer(many=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request', None).user
        validated_data['user'] = user
        cart_item = CartItem.objects.create(**validated_data)
        return cart_item

class OrderSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField('get_discount_percentage')
    class Meta:
        model = Order
        fields = ('id', 'total', 'total_currency', 'sub_total', 'sub_total_currency', 'discount', 'discount_currency', 'discount_percentage' , 'address')
        depth = 1

    def get_discount_percentage(self, order):
        return (order.discount/order.sub_total)*100
