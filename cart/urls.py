# cart/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('api/cart_manage/<int:customer_id>/', CartView.as_view()),
    path('api/cart_manage/<customer_id>/update/<cart_id>/',CartView.as_view()),
    path('api/cart_manage/<customer_id>/delete/<cart_id>/',CartView.as_view()),

]
