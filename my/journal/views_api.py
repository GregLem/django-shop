from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer  # Импорт с правильным именем


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация для API: 20 товаров на странице, можно менять через ?page_size=50"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """
    API для товаров.
    
    Эндпоинты:
    - GET    /api/products/        — список товаров (с пагинацией, фильтрацией, поиском)
    - POST   /api/products/        — создать товар (только авторизованные)
    - GET    /api/products/{id}/   — детали товара
    - PUT    /api/products/{id}/   — полностью обновить товар (только авторизованные)
    - PATCH  /api/products/{id}/   — частично обновить товар (только авторизованные)
    - DELETE /api/products/{id}/   — удалить товар (только авторизованные)
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    
    # Фильтрация, поиск и сортировка
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']              # можно фильтровать: ?category=1
    search_fields = ['name', 'description']      # можно искать: ?search=Мурзилка
    ordering_fields = ['price', 'created_at']    # можно сортировать: ?ordering=price

    def get_permissions(self):
        """
        Создание, изменение и удаление — только для авторизованных.
        Просмотр — для всех.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]