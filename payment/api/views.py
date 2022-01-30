from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
import src.utils as general_utils
from payment.models import CartItem, Order
import payment.utils as utils
from .serializers import *
from djmoney.money import Money
from users.models import Address

class BaseListCreateCartItemView(APIView):

    def get(self, request, format=None):
        cart_items = request.user.cart.all()
        serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data, context={'request': request})
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
