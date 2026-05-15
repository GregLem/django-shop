from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования товара.
    Связана с моделью Product — Django сам знает,
    какие поля создавать и как их сохранять.
    """
    class Meta:
        # Модель, с которой работает форма
        model = Product
        
        # Поля, которые будут показаны в форме
        # (безопаснее перечислить явно, чем использовать '__all__')
        fields = ['name', 'description', 'price', 'category', 'image']
    
    # Русские названия полей (что увидит пользователь)
    labels = {
        'name': 'Название товара',
        'price': 'Цена (в рублях)',
        'description': 'Описание',
        'category': 'Категория',
        'image': 'Изображение',
    }

    # ============================================================
    # ВАЛИДАЦИЯ ЦЕНЫ
    # Django автоматически вызывает clean_<имя_поля>() для каждого поля
    # ============================================================
    def clean_price(self):
        """
        Проверяет, что цена больше нуля.
        Если цена ≤ 0 — форма не пройдёт валидацию,
        и пользователь увидит сообщение об ошибке.
        """
        price = self.cleaned_data.get('price')
        
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть положительной')
        
        return price