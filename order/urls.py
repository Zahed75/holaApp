from django.urls import path
from order.views import *



urlpatterns = [
    path('api/create-order/', create_order),
    path('api/get_all_orders/',get_orders)
]