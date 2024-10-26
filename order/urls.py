from django.urls import path
from order.views import *

urlpatterns = [
    path('api/create-order/', create_order),
    path('api/get_all_orders/', get_orders),
    path('api/update-status/', update_order_status),
    path('api/order_details/<str:order_id>/', get_order_details),
    path('api/initiate-payment/<str:order_id>/', initiate_payment),
    path('api/payment-success/', payment_success),
    path('api/payment-fail/', payment_fail),
    path('api/get-orders/<int:customer_id>/',get_all_orders_by_customer_id),

]
