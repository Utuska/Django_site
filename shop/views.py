from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm
from .models import Category, Product
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from cart.forms import CartAddProductForm


def main_view(request):
    """Главная страница"""
    return render(request, 'shop/main.html') #'shop/index.html')


def product_list(request, category_slug=None):
    """Страница списка товаров"""
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    CONTENT = []
    for product in products:
        CONTENT.append({'id': product.id, 'name': product.name, 'price': product.price, 'available': product.available,
                        'slug': product.slug, 'image': product.image})
    by_page = 8
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, by_page)
    page_index = paginator.get_page(current_page)
    content = page_index.object_list
    if page_index.has_next():
        next_page_url = page_index.next_page_number()
    else:
        next_page_url = current_page
    if page_index.has_previous():
        previous_page_url = page_index.previous_page_number()
    else:
        previous_page_url = current_page
    return render(request, 'shop/list.html', context={
        'products': content,
        'current_page': current_page,
        'prev_page_url': f'?page={previous_page_url}',
        'next_page_url': f'?page={next_page_url}',
    })


def product_detail(request, id, slug):
    """Страница товара"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    content = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/detail.html', content)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('shop:main_view')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def user_logout(request):
    logout(request)
    cart = Cart(request)
    cart.remove_all()
    return redirect('shop:main_view')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:main_view')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'shop/login.html', context)
