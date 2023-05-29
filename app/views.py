import datetime
import time

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import status, viewsets, filters

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Dish, Order, OrderDish
from .permissions import IsManager, IsBotOrAuthenticated
from .serializers import DishSerializer, OrderSerializer


class DishViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Dish objects.
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsManager]


class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Order objects.
    """
    queryset = Order.objects.all().order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsBotOrAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        """
        Get the queryset for Order objects based on user permissions.

        If the user is a superuser, staff, or manager, return all orders. Otherwise, return orders belonging to the user.

        Returns:
            queryset: The filtered queryset of Order objects.
        """
        user = self.request.user
        if not user or (user.is_superuser or user.is_staff or user.groups.filter(name='Manager').exists()):
            return Order.objects.all().order_by('created_at')
        else:
            return Order.objects.filter(user=user).order_by('created_at')

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """
        Process an order by changing its status to 'in_progress', processing the order dishes, and updating the status
        to 'completed' after a delay.

        Args:
            request: The request object.
            pk (int): The primary key of the Order to be processed.

        Returns:
            Response: The response containing the serialized Order data.
        """
        try:
            order = Order.objects.select_for_update().get(id=pk)
            if order.status != 'pending':
                return Response({'error': 'Order has already been processed.'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = 'in_progress'
            order.save()
            with transaction.atomic():
                order_dishes = OrderDish.objects.select_for_update().filter(order=order)
                for order_dish in order_dishes:
                    dish = order_dish.dish
                    quantity = order_dish.quantity
                    if dish.quantity < quantity:
                        order.status = 'canceled'
                        order.save()
                        return Response({'error': f'Insufficient quantity for dish: {dish.name}. Order canceled.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    dish.quantity -= quantity
                    dish.save()
                time.sleep(10)  # Delay for 10 seconds to simulate order processing time
                processed_at = timezone.now()
                order.status = 'completed'
                order.updated_at = processed_at
                order.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)


class MenuView(viewsets.ViewSet):
    """
    Viewset for retrieving the menu (Dish objects).
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieve the list of dishes for the menu.

        Args:
            request: The request object.

        Returns:
            Response: The response containing the serialized Dish data.
        """
        dishes = Dish.objects.filter(quantity__gt=0)
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)
