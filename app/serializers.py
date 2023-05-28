from rest_framework import serializers
from .models import Dish, Order, OrderDish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    dishes = OrderDishSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'special_requests', 'created_at', 'updated_at', 'dishes']

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes')
        order = Order.objects.create(**validated_data)

        for dish_data in dishes_data:
            OrderDish.objects.create(order=order, **dish_data)

        return order
