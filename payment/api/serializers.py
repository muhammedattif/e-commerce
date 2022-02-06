from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from users.api.serializers import UserBasicInfoSerializer
from products.api.serializers import CartProductSerializer
from vendor.api.serializers import StockSerializer
from payment.models import Cart, CartItem
from django.db.models import Sum, F
from decimal import Decimal

UserModel = settings.AUTH_USER_MODEL

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(many=False, read_only=True)
    stock = StockSerializer(many=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        cart_item, created = CartItem.objects.get_or_create(
        product=validated_data['product'],
        stock=validated_data['stock'],
        cart=validated_data['cart']
        )

        if not created:
            cart_item.quantity += validated_data['quantity']
        else:
            cart_item.quantity = validated_data['quantity']
        cart_item.save()
        return cart_item
