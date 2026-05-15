from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, CartItem
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


# ============================================================
# КАТАЛОГ ТОВАРОВ (с пагинацией и подсчётом товаров в категориях)
# ============================================================
def product_list(request):
    # Категории с подсчётом товаров (ОДНИМ запросом, без N+1)
    categories = Category.objects.annotate(product_count=Count('products'))
    
    # Товары с пагинацией (12 штук на странице)
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'title': 'Catalog of goods'
    }
    return render(request, 'journal/product_list.html', context)


# ============================================================
# СОЗДАНИЕ ТОВАРА (только для staff)
# ============================================================
@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()        # убрали commit=False — не нужно
            messages.success(request, f"Товар {product.name} успешно создан!")
            return redirect('product_list')
        else:
            messages.error(request, 'Исправляй ошибки в форме!')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Добавление товара'
    }
    return render(request, 'journal/product_form.html', context)


# ============================================================
# ПОЛУЧЕНИЕ ИЛИ СОЗДАНИЕ КОРЗИНЫ (для пользователя или сессии)
# ============================================================
def get_or_create_cart(request):
    if request.user.is_authenticated:
        # Корзина для залогиненного пользователя
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        # Корзина для анонима (по ключу сессии)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart


# ============================================================
# ДОБАВЛЕНИЕ ТОВАРА В КОРЗИНУ
# ============================================================
@login_required(login_url='/accounts/login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_detail')


# ============================================================
# ПРОСМОТР КОРЗИНЫ
# ============================================================
def cart_detail(request):
    cart = get_or_create_cart(request)
    # select_related('product') — чтобы не делать лишних запросов к товарам
    items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'journal/cart_detail.html', context)


# ============================================================
# УДАЛЕНИЕ ТОВАРА ИЗ КОРЗИНЫ
# ============================================================
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


# ============================================================
# ОБНОВЛЕНИЕ КОЛИЧЕСТВА ТОВАРА В КОРЗИНЕ
# ============================================================
def update_cart_quantity(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1                   # если ввели не число — ставим 1
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart_detail')


# ============================================================
# ДЕТАЛЬНАЯ СТРАНИЦА ТОВАРА
# ============================================================
def product_detail(request, pk):
    # select_related('category') — чтобы не делать лишний запрос к категории
    product = get_object_or_404(Product.objects.select_related('category'), id=pk)
    context = {
        'product': product,
    }
    return render(request, 'journal/product_detail.html', context)