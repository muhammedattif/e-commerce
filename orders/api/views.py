from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import *
from orders.models import Order
import src.utils as general_utils

class OrdersListCreateView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderRetriveUpdateView(APIView):

    def get(self, request, id):
        user = request.user
        try:
            order = Order.objects.get(id=id, user=user)
            serializer = OrderDetailSerializer(order, many=False)
            return Response(serializer.data)
        except Order.DoesNotExist:
            error = general_utils.error('obj_not_found')
            return Response(error, status=status.HTTP_404_NOT_FOUND)

class OrderCancellingView(APIView):

    def put(self, request, id):
        user = request.user
        try:
            order = Order.objects.prefetch_related('items', 'items__stock__product').get(id=id, user=user)
            order.cancel()
            success = general_utils.success('updated_successfully')
            return Response(success)
        except Order.DoesNotExist:
            error = general_utils.error('obj_not_found')
            return Response(error, status=status.HTTP_404_NOT_FOUND)
