from django.urls import path
from order.views import *



urlpatterns = [
    path('api/create-order/', create_order),
]