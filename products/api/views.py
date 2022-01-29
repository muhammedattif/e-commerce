from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework import parsers
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
import src.utils as general_utils
from products.models import Product, ProductImage, Feature, FeatureAttribute
import products.utils as utils
from .serializers import *
from src.custom_permissions import IsPostOrIsAuthenticated
import json
from rest_framework.generics import ListAPIView
from django.db.models import Q
from functools import reduce
import operator
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters



class ProductFilter(ListAPIView):
    permission_classes = ()
    queryset = Product.objects.select_related('category', 'brand', 'vendor').prefetch_related('features__attributes', 'category__childs', 'images', 'reviews').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name', 'brand__name', 'price']
    ordering_fields = ['price', 'creation']


class BaseListCreateProductView(APIView, PageNumberPagination):

    permission_classes=(IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.all()
        products = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        if not request.user.is_authenticated or not request.user.is_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        product_images = request.data.getlist('images')
        body = json.loads(request.data['body'])

        vendor = request.user
        features = body.pop('features')
        product = Product.objects.create(vendor=vendor, **body)

        images_obj = []
        features_obj = []
        attributes_obj = []

        for image in product_images:
            product_image_instance = ProductImage(product=product, image=image)
            images_obj.append(product_image_instance)

        for feature in features:
            attributes = feature.pop('attributes')
            feature_instance = Feature(product=product, **feature)

            for attribute in attributes:
                attribute_instance = FeatureAttribute(feature=feature_instance, **attribute)
                attributes_obj.append(attribute_instance)

            features_obj.append(feature_instance)

        print(1)
        ProductImage.objects.bulk_create(images_obj)
        Feature.objects.bulk_create(features_obj)
        FeatureAttribute.objects.bulk_create(attributes_obj)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):

    def get(self, request, id):
        product, found, error = utils.get_product(id, select_related=['category', 'vendor'], prefetch_related=['features__attributes', 'images', 'reviews'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = SingleProductSerializer(product, many=False, context={'request': request})
        return Response(serializer.data)



class ReviewsListCreateView(APIView):

    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, id):
        product, found, error = utils.get_product(id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):

        product, found, error = utils.get_product(id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data.update({
            'user': request.user.id,
            'product': product.id
        })

        serializer = ReviewCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review = serializer.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckReview(APIView):

    def get(self, request, id):
        response = {}
        try:
            review = Review.objects.filter(user=request.user, product_id=id).first()
            response['reviewd'] = True
        except Review.DoesNotExist:
            response['reviewd'] = False

        return Response(response)
