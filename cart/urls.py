# cart/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('api/cart_manage/<int:customer_id>/', CartView.as_view()),
    path('api/cart_manage/<customer_id>/update/<cart_id>/', CartView.as_view()),
    path('api/cart_manage/<customer_id>/delete/<cart_id>/', CartView.as_view()),
    path('api/get_all_carts/<customer_id>/', get_all_carts_by_id),
    path('api/apply-coupon/', apply_coupon)
]
