import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, Dish
from .serializers import OrderSerializer

User = get_user_model()


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        """
        Test creating a new order.
        """
        dish = Dish.objects.create(name='Pizza', price=10.99, quantity=5)
        data = {
            'special_requests': 'Extra sauce',
            'dishes': [
                {
                    'id': dish.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post('/api/orders/', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data['id'])
        serializer = OrderSerializer(order)
        self.assertEqual(response.data, serializer.data)

    def test_create_empty_order(self):
        """
        Test creating a new order.
        """
        data = {
            'special_requests': 'Extra sauce',
            'dishes': []
        }
        response = self.client.post('/api/orders/', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_quantity(self):
        """
        Test creating a new order with insufficient quantity of dishes.
        """
        dish = Dish.objects.create(name='Pizza', price=10.99, quantity=5)
        data = {
            'special_requests': 'Extra sauce',
            'dishes': [
                {
                    'id': dish.id,
                    'quantity': 10
                }
            ]
        }
        response = self.client.post('/api/orders/', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_order_already_processed(self):
        """
        Test processing an order that is already processed.
        """
        order = Order.objects.create(user=self.user, status='completed')
        response = self.client.post(f'/api/orders/{order.id}/process/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_order_not_found(self):
        """
        Test processing an order that doesn't exist.
        """
        response = self.client.post('/api/orders/9999/process/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DishTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_dish(self):
        """
        Test creating a new dish.
        """
        data = {
            'name': 'Pizza',
            'description': 'A delicious pizza.',
            'price': 10.99,
            'quantity': 10,
        }
        response = self.client.post('/api/dishes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        dish = Dish.objects.get(pk=response.data['id'])
        self.assertEqual(dish.name, 'Pizza')

    def test_create_dish_not_manager(self):
        """
        Test creating a new dish as a non-manager.
        """
        self.user.is_superuser = False
        self.user.save()
        data = {
            'name': 'Pizza',
            'description': 'A non-delicious pizza.',
            'price': 10.99,
            'quantity': 10
        }
        response = self.client.post('/api/dishes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
