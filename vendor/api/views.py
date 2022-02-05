from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product, Review, Feature, FeatureAttribute
from products.api.serializers import ReviewSerializer, VendorProductsSerializer, VendorReviewsSerializer, FeatureSerializer
from payment.api.serializers import VendorOrderItemSerializer
from payment.models import OrderItem
from products import utils as product_utils
import src.utils as general_utils
from .serializers import StockSerializer, StockItemSerializer
from vendor.models import Stock
from django.db.models import Sum, F, Count, Q
from django.db.utils import IntegrityError
from django.db import transaction

class VendorProductList(ListAPIView):
    serializer_class = VendorProductsSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand', 'vendor'
        ).prefetch_related('features__attributes', 'category__childs', 'images', 'reviews'
        ).filter(vendor=self.request.user)
        return queryset


class VendorProductReviewsList(ListAPIView):
    serializer_class = VendorReviewsSerializer

    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product').filter(product__vendor=self.request.user)
        return queryset

class VendorOrderList(ListAPIView):

    serializer_class = VendorOrderItemSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.filter(product__vendor=self.request.user)
        return queryset

class StockAPIView(ListAPIView):
    serializer_class = StockItemSerializer

    # TODO: Change it to use product.get_quantity
    def get_queryset(self):
        queryset = Stock.objects.select_related('product').values('product').filter(product__vendor=self.request.user).annotate(quantity=Sum(F('quantity')))
        return queryset


class StockCreateListRetriveAPIView(APIView):

    def get(self, request, id):

        product, found, error = product_utils.get_product(id, select_related=['category', 'vendor'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        product_stock = Stock.objects.prefetch_related('attributes').filter(product=product)
        serializer = StockSerializer(product_stock, many=True)
        return Response(serializer.data)

    def put(self, request, id):

        if not ('stock_id' and 'quantity') in request.data:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)

        stock_id = request.data['stock_id']
        quantity = request.data['quantity']

        updated = Stock.objects.filter(id=stock_id, product__id=id).update(quantity=quantity)
        if not updated:
            return Response(general_utils.error('not_updated'), status=status.HTTP_400_BAD_REQUEST)

        success_response = general_utils.success('updated_successfully')
        return Response(success_response)


    @transaction.atomic
    def post(self, request, id):

        if not request.user.is_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        if 'attributes' not in request.data:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)

        attributes = request.data['attributes']
        product, found, error = product_utils.get_product(id, select_related=['category', 'vendor'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        # Check if attribues belongs to this product
        product_attributes = FeatureAttribute.objects.filter(feature__product=product).values_list('id', flat=True)
        if attributes:
            match = set(attributes).issubset(product_attributes)
            if not match:
                return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)



        try:
            stock = Stock.objects.create(product=product)
            stock.attributes.set(attributes)
        except IntegrityError as e:
            error = general_utils.error('stock_already_exists', error_description=str(e))
            return Response(error)

        serializer = StockSerializer(stock, many=False)
        return Response(serializer.data)


class ProductStockFeaturesAPIView(APIView):

    def get(self, request, id):

        if not request.user.is_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        product, found, error = product_utils.get_product(id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        features = Feature.objects.prefetch_related('attributes').annotate(attributes_num=Count('attributes')).filter(product=product, attributes_num__gt=1)
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)
