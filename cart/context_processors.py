from .cart import Cart
from shop.models import Category


def cart(request):
    categories = Category.objects.all()
    return {'cart': Cart(request), 'categories': categories}
