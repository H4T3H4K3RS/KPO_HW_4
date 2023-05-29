from django.db.models import F
from rest_framework import serializers
from .models import Dish, Order, OrderDish


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dish model.
    """

    class Meta:
        model = Dish
        fields = '__all__'


class OrderDishSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderDish model.
    """

    class Meta:
        model = OrderDish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    dishes = OrderDishSerializer(many=True, read_only=True, source='orderdish_set')
    user = serializers.ReadOnlyField(source='user.id')
    status = serializers.CharField(read_only=True)
    special_requests = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'special_requests', 'created_at', 'updated_at', 'dishes']

    def create(self, validated_data):
        """
        Create a new Order instance.

        Args:
            validated_data (dict): The validated data for creating the Order.

        Returns:
            Order: The created Order instance.

        Raises:
            serializers.ValidationError: If there are validation errors during order creation.
        """
        dishes_data = self.initial_data.get('dishes', [])
        if len(dishes_data) == 0:
            raise serializers.ValidationError('Order must contain at least one dish.')
        user = self.context['request'].user
        order = Order.objects.create(user=user, status='pending', **validated_data)
        for dish_data in dishes_data:
            dish_id = dish_data.get('id')
            quantity = dish_data.get('quantity')

            dish = Dish.objects.filter(id=dish_id)
            if dish.exists():
                if dish.first().quantity < quantity:
                    order.delete()
                    raise serializers.ValidationError(
                        f'Insufficient quantity for dish: {dish.first().name}. Order canceled.')
            else:
                order.delete()
                raise serializers.ValidationError(f'Dish with id {dish_id} does not exist.')
            OrderDish.objects.create(order=order, dish=dish.first(), quantity=quantity, price=dish.first().price)

        return order
