from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import src.utils as general_utils
from payment.models import CartItem
import payment.utils as utils
from .serializers import *

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
