from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name="product_create"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:item_id>', views.remove_from_cart, name="remove_from_cart"),
    path('update-cart/<int:item_id>', views.update_cart_quantity, name="update_cart_quantity"),
]
