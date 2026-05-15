from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий — превращает Category в JSON и обратно"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):  # Опечатка в названии: ProductSerialaizer → ProductSerializer
    """
    Сериализатор для товаров.
    Добавляет вложенную категорию и форматированную цену.
    """
    # Вложенный сериализатор — показывает полную информацию о категории
    category_detail = CategorySerializer(source='category', read_only=True)
    
    # Кастомное поле — цена с "руб" на конце
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'formatted_price',
            'category', 'category_detail', 'description', 'created_at'
        ]
        read_only_fields = ['created_at', 'price']  # цену нельзя менять через API

    def get_formatted_price(self, obj):
        """Возвращает цену в читаемом формате: '100.00 руб'"""
        return f"{obj.price} руб"