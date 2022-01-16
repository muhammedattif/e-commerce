from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction

from users.models import User
from products.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discount', 'quantity')

    def create(self, validated_data):
        user = self.context.get('request', None).user
        validated_data['provider'] = user
        product = Product.objects.create(**validated_data)
        return product
