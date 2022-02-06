from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
import src.utils as general_utils
from payment.models import Cart, CartItem
from orders.models import Order, OrderItem
import payment.utils as utils
from .serializers import *
from orders.api.serializers import OrderSerializer
from djmoney.money import Money
from users.models import Address
from vendor.models import Stock
from django.db import transaction


class BaseListCreateCartItemView(APIView):

    def get(self, request, format=None):
        cart = Cart.objects.prefetch_related('items__product', 'items__stock__options').get(user=request.user)
        cart.recalculate_cart_amount()
        serializer = CartSerializer(cart, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request):

        data = request.data
        data.update({'cart': request.user.cart.id})

        try:
            stock = Stock.objects.get(
            id=data['stock'],
            product__id=data['product']
            )
        except Stock.DoesNotExist:
            error = general_utils.error('invalid_params')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if data['quantity'] > stock.quantity:
            error = general_utils.error('product_not_available')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item = serializer.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemView(APIView):

    def put(self, request, id):

        quantity = request.data['quantity']

        try:
            cart_item = CartItem.objects.select_related('stock').get(id=id, cart=request.user.cart)
        except CartItem.DoesNotExist:
            error = general_utils.error('invalid_url')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if quantity > cart_item.stock.quantity:
            error = general_utils.error('product_not_available')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        success = general_utils.success('updated_successfully')
        return Response(success)

    def delete(self, request, id):

        try:
            cart_item = CartItem.objects.get(id=id, cart=request.user.cart)
        except CartItem.DoesNotExist:
            error = general_utils.error('invalid_url')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        cart_item.delete()
        success = general_utils.success('deleted_successfully')
        return Response(success)


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

        cart = Cart.objects.get(user=request.user)

        # Get cart items
        cart_items = CartItem.objects.select_related('stock', 'product', 'cart').prefetch_related('stock__product').filter(cart=cart)
        if not cart_items:
            error = general_utils.error('empty_cart')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Check if all items quantity available
        for item in cart_items:
            if item.quantity > item.stock.quantity:
                error = general_utils.error('invalid_quantity_value',
                product_name=item.product.name,
                available_quantity=item.stock.quantity
                )
                return Response(error, status=status.HTTP_404_NOT_FOUND)

        cart.recalculate_cart_amount()

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
            item.stock.quantity = F('quantity') - item.quantity
            item.stock.save()

        OrderItem.objects.bulk_create(order_items_objs)
        cart.clear()
        serializer = OrderSerializer(order, many=False)
        data = serializer.data
        return Response(data)
