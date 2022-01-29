from rest_framework import serializers
from categories.models import Category, Brand

class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    childs = ChildCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'childs')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
