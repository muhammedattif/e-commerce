from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
import src.utils as general_utils
from payment.models import Cart, CartItem, Order
import payment.utils as utils
from .serializers import *
from djmoney.money import Money
from users.models import Address
from products.models import FeatureAttributesMap

class BaseListCreateCartItemView(APIView):

    def get(self, request, format=None):
        cart = Cart.objects.prefetch_related('items__product__reviews', 'items__attributes_map__attributes').get(user=request.user)
        serializer = CartSerializer(cart, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request):

        data = request.data
        data.update({'cart': request.user.cart.id})

        valid_attributes_map = FeatureAttributesMap.objects.filter(
        id=data['attributes_map'],
        product__id=data['product']
        ).exists()

        if not valid_attributes_map:
            error = general_utils.error('invalid_params')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item = serializer.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckoutView(APIView):

    def post(self, request):

        try:
            address_id = request.data['address_id']
            address = Address.objects.get(id=address_id, user=request.user)
        except Exception as e:
            error = general_utils.error('invalid_params')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.select_related('user','product').filter(user=request.user)
        cart_items_sub_total = cart_items.aggregate(sum=Sum('product__price'))['sum']
        cart_items_discounts = cart_items.aggregate(sum=Sum('product__discount'))['sum']
        cart_items_total = cart_items_sub_total - cart_items_discounts
        order = Order.objects.create(
                user=request.user,
                total=Money(cart_items_total, 'SAR'),
                sub_total=Money(cart_items_sub_total, 'SAR'),
                discount=Money(cart_items_discounts, 'SAR'),
                address=address
         )

        order.items.set(cart_items)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
