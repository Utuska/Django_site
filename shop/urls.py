from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('product_detail/<int:id>/<slug>', views.product_detail, name='product_detail'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('main/', views.main_view, name='main_view'),
    path('product_list/<category_slug>/', views.product_list, name='product_list_category'),
    path('product_list/', views.product_list, name='product_list')
]
