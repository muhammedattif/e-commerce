from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product, Review, Feature, FeatureOption
from products.api.serializers import ReviewSerializer, VendorProductsSerializer, VendorProductSerializer, VendorReviewsSerializer, FeatureSerializer
from orders.api.serializers import VendorOrderItemSerializer
from orders.models import Order, OrderItem
from products import utils as product_utils
import src.utils as general_utils
from .serializers import (
StockSerializer,
StockItemSerializer,
ReportSerializer,
VendorSerlializer,
VendorProductUpdateSerializer,
JoinFormSerializer
)
from vendor.models import Stock, JoinForm
from django.db.models import Sum, F, Count, Q
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters

User = get_user_model()

class VendorProductList(ListAPIView):
    serializer_class = VendorProductsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name', 'brand__name', 'price']
    ordering_fields = ['price', 'creation']

    def get_queryset(self):
        queryset = Product.objects.filter(vendor=self.request.user)
        return queryset

class VendorsList(ListAPIView):
    serializer_class = VendorSerlializer
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.filter(vendor_status__is_active=True)
        return queryset

class VendorProductDetail(APIView):
    def get(self, request, id):

        try:
            product = Product.objects.select_related('category', 'brand', 'vendor'
            ).prefetch_related('features__options', 'category__childs', 'images', 'reviews'
            ).get(id=id, vendor=self.request.user)
        except Product.DoesNotExist:
            error = general_utils.error('product_not_found')
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorProductSerializer(product, many=False)
        return Response(serializer.data)

    def put(self, request, id):

        try:
            product = Product.objects.get(id=id, vendor=self.request.user)
        except Product.DoesNotExist:
            error = general_utils.error('product_not_found')
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorProductUpdateSerializer(product, data=request.data, many=False, context = {
          'request': request
        })

        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)


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

class StockAPIView(APIView):

    def get(self, request):
        stock_items = Product.objects.filter(~Q(stock=None), vendor=request.user).annotate(quantity=Sum(F('stock__quantity')))
        serializer = StockItemSerializer(stock_items, many=True)
        return Response(serializer.data)


class StockCreateListRetriveAPIView(APIView):

    def get(self, request, id):

        filter_kwargs = {
        'id': id,
        'vendor': request.user
        }
        product, found, error = product_utils.get_product(filter_kwargs, select_related=['category', 'vendor'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        product_stock = Stock.objects.prefetch_related('options').filter(product=product)
        serializer = StockSerializer(product_stock, many=True)
        return Response(serializer.data)

    def put(self, request, id):

        if not request.user.is_active_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        if not ('stock_id' and 'quantity') in request.data:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)

        stock_id = request.data['stock_id']
        quantity = request.data['quantity']

        updated = Stock.objects.filter(id=stock_id, product__id=id, product__vendor=request.user).update(quantity=quantity)
        if not updated:
            return Response(general_utils.error('not_updated'), status=status.HTTP_400_BAD_REQUEST)

        success_response = general_utils.success('updated_successfully')
        return Response(success_response)


    @transaction.atomic
    def post(self, request, id):

        if not request.user.is_active_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        if not ('options' and 'quantity') in request.data:
            return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)

        options = request.data['options']
        quantity = request.data['quantity']
        filter_kwargs = {
        'id': id,
        'vendor': request.user
        }
        product, found, error = product_utils.get_product(filter_kwargs, select_related=['category', 'vendor'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if options:
            # Check if options belongs to this product
            product_options = FeatureOption.objects.filter(feature__product=product).values_list('id', flat=True)
            match = set(options).issubset(product_options)
            if not match:
                return Response(general_utils.error('invalid_params'), status=status.HTTP_400_BAD_REQUEST)
        else:
            exists = Stock.objects.filter(product=product, options=None)
            if exists:
                error = general_utils.error('stock_already_exists')
                return Response(error, status=status.HTTP_409_CONFLICT)
        try:
            stock = Stock.objects.create(product=product, quantity=quantity)
            stock.options.set(options)
        except IntegrityError as e:
            error = general_utils.error('stock_already_exists', error_description=str(e))
            return Response(error, status=status.HTTP_409_CONFLICT)

        serializer = StockSerializer(stock, many=False)
        return Response(serializer.data)


class ProductStockFeaturesAPIView(APIView):

    def get(self, request, id):

        if not request.user.is_active_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        filter_kwargs = {
        'id': id,
        'vendor': request.user
        }
        product, found, error = product_utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        features = Feature.objects.prefetch_related('options').annotate(options_num=Count('options')).filter(product=product, options_num__gt=1)
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

class Report(APIView):

    def get(self, request):

        if not request.user.is_active_vendor:
            return Response(general_utils.error('not_vendor'), status=status.HTTP_403_FORBIDDEN)

        number_of_orders = Order.objects.select_related('user').filter(items__product__vendor=request.user).count()
        items = OrderItem.objects.filter(product__vendor=request.user)

        orders_amount = items.aggregate(sum=Sum(F('price') - F('discount')))['sum']

        received_payments = items.filter(order__is_paid=True).aggregate(sum=Sum(F('price') - F('discount')))['sum']
        if not received_payments:
            received_payments = 0

        number_of_items_sold = items.count()
        sales = items.values('creation').annotate(total=Sum(F('price') - F('discount'))).order_by('creation')

        order_days = items.values_list('creation', flat=True).distinct().count()
        if orders_amount:
            daily_sales = orders_amount/order_days
        else:
            orders_amount = 0
            daily_sales = 0

        data = {
        'number_of_orders': number_of_orders,
        'orders_amount': orders_amount,
        'number_of_items_sold': number_of_items_sold,
        'received_payments': received_payments,
        'sales': sales,
        'daily_sales': daily_sales,
        }

        serializer = ReportSerializer(data, many=False)
        return Response(serializer.data)


class JoinRequest(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = JoinFormSerializer
    queryset = JoinForm.objects.all()
