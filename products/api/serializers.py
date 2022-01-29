from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction

from users.api.serializers import UserBasicInfoSerializer
from users.models import User
from products.models import Product, Review, Feature, FeatureAttribute


class FeatureAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureAttribute
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    attributes = FeatureAttributeSerializer(many=True, read_only=True)
    class Meta:
        model = Feature
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_rating')
    provider = UserBasicInfoSerializer(many=False, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount', 'quantity', 'rating', 'features', 'provider', 'creation')

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discount', 'quantity')

class ReviewSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer(many=False, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('user', None)
        product = self.context.get('product', None)
        validated_data['user'] = user
        validated_data['product'] = product
        review = Review.objects.create(**validated_data)
        return review

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review
