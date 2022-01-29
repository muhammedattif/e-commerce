from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

from users.api.serializers import UserBasicInfoSerializer
from products.api.serializers import ProductsSerializer
from payment.models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=False, read_only=True)
    class Meta:
        model = CartItem
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
