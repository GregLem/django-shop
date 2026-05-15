from django.contrib import admin

# Register your models here.
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at', 'updated_at', 'image')
    list_filter = ('category', 'created_at', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_per_page = 20

    fieldsets = (
        ('Основная инфо', {
            'fields': ('name', 'category', 'price', 'image')
        }),
        ('Детали', {
            'classes': ('collapse',),
            'fields': ('description',)
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
