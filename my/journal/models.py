from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', help_text='Type the name of category')
    description = models.TextField(verbose_name="Description", blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Product Name')
    description = models.TextField(verbose_name="description", blank=True)
    image = models.ImageField(upload_to='products/', verbose_name='Image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date of change')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']                    # новые товары сверху
        indexes = [models.Index(fields=['name', 'category'])]

    def __str__(self):
        return f"{self.name} {self.price}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username}"
        return f"сессия {self.session_key}"
    
    # Общая сумма корзины
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    # Общее количество товаров в корзине (берём из учебной версии)
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Фиксация цены на момент добавления (наша доработка)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # При создании фиксируем цену
        if not self.pk and self.price_at_addition is None:
            self.price_at_addition = self.product.price
        super().save(*args, **kwargs)

    def total_price(self):
        # Используем зафиксированную цену, если она есть
        if self.price_at_addition is not None:
            return self.price_at_addition * self.quantity
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"