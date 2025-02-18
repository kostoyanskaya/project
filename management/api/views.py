from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import OrderSerializer
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Order.  Предоставляет CRUD операции
    и endpoint для расчета выручки.
    """

    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

    def get_object(self):
        """
        Переопределяет метод get_object() для возврата
        кастомного сообщения при отсутствии объекта.
        """
        return get_object_or_404(Order, id=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяет метод destroy() для возврата
        кастомного ответа при удалении заказа.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Заказ успешно удален."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def total_revenue(self, request):
        """
        Endpoint для расчета общей выручки по оплаченным заказам.
        """
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = sum(order.total_price for order in paid_orders)
        return Response({'total_revenue': total_revenue})

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint для поиска заказов по номеру стола или статусу.
        """
        query = request.query_params.get('q', None)
        if query:
            orders = Order.objects.filter(
                models.Q(table_number__icontains=query) |
                models.Q(status__icontains=query)
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

        return Response(
            {"message": "Укажите поисковой запрос (параметр 'q')."},
            status=status.HTTP_400_BAD_REQUEST
        )
