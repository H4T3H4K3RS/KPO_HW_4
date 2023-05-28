from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dish, Order, OrderDish
from .permissions import ManagerPermission
from .serializers import DishSerializer, OrderSerializer


class DishListView(APIView):
    permission_classes = [IsAuthenticated, ManagerPermission]

    def get(self, request):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            dish = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetailView(APIView):
    permission_classes = [IsAuthenticated, ManagerPermission]

    def get(self, request, dish_id):
        try:
            dish = Dish.objects.get(id=dish_id)
            serializer = DishSerializer(dish)
            return Response(serializer.data)
        except Dish.DoesNotExist:
            return Response({'error': 'Dish not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, dish_id):
        try:
            dish = Dish.objects.get(id=dish_id)
            serializer = DishSerializer(dish, data=request.data)
            if serializer.is_valid():
                dish = serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Dish.DoesNotExist:
            return Response({'error': 'Dish not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, dish_id):
        try:
            dish = Dish.objects.get(id=dish_id)
            dish.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dish.DoesNotExist:
            return Response({'error': 'Dish not found.'}, status=status.HTTP_404_NOT_FOUND)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderProcessingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            # TODO: order processing logic here
            order.status = 'completed'
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)


class MenuView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dishes = Dish.objects.filter(quantity__gt=0)
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)
