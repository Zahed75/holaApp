from django.urls import path
from order.views import *

urlpatterns = [
    path('api/create-order/', create_order),
    path('api/get_all_orders/', get_orders),
    path('api/update-status/', update_order_status),
    path('api/order_details/<str:order_id>/', get_order_details)


]