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
from products.models import Product, ProductImage, Review, Feature, FeatureAttribute, FeatureAttributesMap
from categories.api.serializers import BrandSerializer, CategorySerializer

class FeatureAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureAttribute
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    attributes = FeatureAttributeSerializer(many=True, read_only=True)
    class Meta:
        model = Feature
        fields = ('id', 'name', 'type', 'attributes')

class FeatureAttributesMapSerializer(serializers.ModelSerializer):
    attributes = FeatureAttributeSerializer(many=True, read_only=True)
    class Meta:
        model = FeatureAttributesMap
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

class ProductsSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_rating')
    discount_percentage = serializers.SerializerMethodField('get_discount_percentage')
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount', 'discount_percentage', 'rating', 'creation')

    def get_discount_percentage(self, product):
        return (product.discount/product.price)*100

class CartProductSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField('get_discount_percentage')
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'discount', 'discount_percentage')

    def get_discount_percentage(self, product):
        return (product.discount/product.price)*100

class SingleProductSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_rating')
    vendor = UserBasicInfoSerializer(many=False, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    relevant_products = serializers.SerializerMethodField('get_relevant_products')
    discount_percentage = serializers.SerializerMethodField('get_discount_percentage')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount', 'discount_percentage', 'rating', 'features', 'category', 'brand', 'images', 'vendor', 'creation', 'relevant_products')


    def get_relevant_products(self, product):
        products = ProductsSerializer(product.get_relevant_products(), many=True)
        return products.data

    def get_discount_percentage(self, product):
        return (product.discount/product.price)*100

class VendorProductsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount', 'features', 'category', 'brand', 'images')

class VendorReviewsSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer(many=False, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        depth = 1

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discount')

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
