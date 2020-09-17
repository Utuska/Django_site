from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('remove/<product_id>', views.cart_remove, name='cart_remove'),
    path('add/<product_id>', views.cart_add, name='cart_add'),
]
