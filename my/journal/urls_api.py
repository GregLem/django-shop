from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProductViewSet


# Роутер автоматически создаёт все URL'ы для ViewSet'а
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]