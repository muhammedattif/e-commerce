from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
import src.utils as general_utils
from products.models import Product, ProductImage, Feature, FeatureOption
from vendor.models import Stock
import products.utils as utils
from .serializers import *
from src.custom_permissions import IsGetOrIsAuthenticated
import json
from rest_framework.generics import ListAPIView
from django.db.models import Q, Count, Sum, F
from functools import reduce
import operator
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters



class ProductFilter(ListAPIView):
    permission_classes = ()
    queryset = Product.objects.select_related('category', 'brand', 'vendor').prefetch_related('features__options', 'category__childs', 'images', 'reviews').all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name', 'brand__name', 'price']
    ordering_fields = ['price', 'creation']


class BaseListCreateProductView(APIView, PageNumberPagination):

    permission_classes=(IsGetOrIsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.prefetch_related('reviews').all()
        products = self.paginate_queryset(products, request, view=self)
        serializer = ProductsSerializer(products, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        if not request.user.is_authenticated or not request.user.is_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        product_images = request.data.getlist('images')
        body = json.loads(request.data['body'])

        vendor = request.user
        features = body.pop('features')

        # TODO: Wrap try and Catch
        product = Product.objects.create(vendor=vendor, **body)

        images_obj = []
        features_obj = []
        options_obj = []

        for image in product_images:
            product_image_instance = ProductImage(product=product, image=image)
            images_obj.append(product_image_instance)

        for feature in features:
            options = feature.pop('options')
            feature_instance = Feature(product=product, **feature)

            for option in options:
                option_instance = FeatureOption(feature=feature_instance, **option)
                options_obj.append(option_instance)

            features_obj.append(feature_instance)

        ProductImage.objects.bulk_create(images_obj)
        Feature.objects.bulk_create(features_obj)
        FeatureOption.objects.bulk_create(options_obj)
        serializer = ProductsSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    permission_classes = ()

    def get(self, request, id):
        filter_kwargs = {
        'id': id
        }
        product, found, error = utils.get_product(filter_kwargs, select_related=['category', 'vendor'], prefetch_related=['features__options', 'images', 'reviews', 'category__products__reviews'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = SingleProductSerializer(product, many=False, context={'request': request})
        return Response(serializer.data)


class ReviewsListCreateView(APIView):

    permission_classes = (IsGetOrIsAuthenticated,)

    def get(self, request, id):
        filter_kwargs = {
        'id': id
        }
        product, found, error = utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):

        filter_kwargs = {
        'id': id
        }
        product, found, error = utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        # TODO: Enhance
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
            Review.objects.filter(user=request.user, product_id=id).first()
            response['reviewd'] = True
        except Review.DoesNotExist:
            response['reviewd'] = False

        return Response(response)

class ProductAvailability(APIView):

    def post(self, request, id):

        if 'options' not in request.data:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)

        options = request.data['options']
        options_len = len(options)

        quantity = 1
        if 'quantity' in request.data:
            quantity = request.data['quantity']


        filter_kwargs = {
        'id': id
        }
        product, found, error = utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        try:
            stock = Stock.objects.annotate(
                                            total_options=Count('options'),
                                            matching_options=Count('options', filter=Q(options__in=options))
                                        ).filter(
                                            product__id=id,
                                            matching_options=options_len,
                                            total_options=options_len
                                        ).first()
            if not stock:
                return Response(general_utils.error('product_not_available'), status=status.HTTP_404_NOT_FOUND)

            if not stock.quantity or stock.quantity < quantity:
                return Response(general_utils.error('out_of_stock'), status=status.HTTP_404_NOT_FOUND)

            features_additional_price = FeatureOption.objects.filter(id__in=options).aggregate(sum=Sum(F('additional_price')))['sum']
            new_price = (features_additional_price + product.price.amount)* quantity

            response = general_utils.success('product_available', new_price=new_price, stock_id=stock.id)

            return Response(response)

        except ValueError:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)
