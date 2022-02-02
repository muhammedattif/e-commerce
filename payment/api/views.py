from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
import src.utils as general_utils
from payment.models import Cart, CartItem, Order, OrderItem
import payment.utils as utils
from .serializers import *
from djmoney.money import Money
from users.models import Address
from vendor.models import Stock
from django.db import transaction

class BaseListCreateCartItemView(APIView):

    def get(self, request, format=None):
        cart = Cart.objects.prefetch_related('items__product', 'items__stock__attributes').get(user=request.user)
        cart.recalculate_cart_amount()
        serializer = CartSerializer(cart, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request):

        data = request.data
        data.update({'cart': request.user.cart.id})

        valid_stock = Stock.objects.filter(
        id=data['stock'],
        product__id=data['product']
        ).exists()

        if not valid_stock:
            error = general_utils.error('invalid_params')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item = serializer.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckoutView(APIView):

    @transaction.atomic
    def post(self, request):

        try:
            address_id = request.data['address_id']
            address = Address.objects.get(id=address_id, user=request.user)
        except KeyError:
            error = general_utils.error('invalid_params')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        except Address.DoesNotExist:
            error = general_utils.error('invalid_address')
            return Response(error, status=status.HTTP_404_NOT_FOUND)


        cart = Cart.objects.prefetch_related('items__product', 'items__stock__attributes').get(user=request.user)

        # Get cart items
        cart_items = cart.items.all()

        if not cart_items:
            error = general_utils.error('empty_cart')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
                user=request.user,
                total=cart.total,
                sub_total=cart.sub_total,
                discount=cart.discount,
                taxes=cart.taxes,
                address=address
         )

        order_items_objs = []

        for item in cart_items:
            order_item_instance = OrderItem(
            product=item.product,
            order=order,
            stock=item.stock,
            quantity=item.quantity
            )
            order_items_objs.append(order_item_instance)

        OrderItem.objects.bulk_create(order_items_objs)
        cart.clear()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
