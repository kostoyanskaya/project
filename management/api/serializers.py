from typing import List, Dict

from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    """

    class Meta:
        model = Order
        fields = '__all__'

    def validate_items(self, items: List[Dict]) -> List[Dict]:
        """
        Валидирует список блюд. Проверяет, что каждое блюдо
        имеет 'name' и 'price', а цена - положительное число.
        """
        for item in items:
            if not isinstance(item, dict):
                raise serializers.ValidationError(
                    "Каждый элемент списка блюд должен быть словарем."
                )
            if 'name' not in item or 'price' not in item:
                raise serializers.ValidationError(
                    "Каждый элемент должен содержать ключи 'name' и 'price'."
                )
            if not isinstance(item['name'], str):
                raise serializers.ValidationError(
                    "Название блюда должно быть строкой."
                )
            if (not isinstance(item['price'], (int, float)) or
                    item['price'] <= 0):
                raise serializers.ValidationError(
                    "Цена блюда должна быть положительным числом."
                )
        return items
