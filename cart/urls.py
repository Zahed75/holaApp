# cart/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('api/add_cart/', add_to_cart),
    path('api/update_cart/<cart_id>/', edit_cart),
    path('api/delete_cart/<cart_id>/', delete_cart_item),
    path('api/get_carts_customer/<customer_id>/',get_all_carts_by_customer)

]
