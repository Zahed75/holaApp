from django.urls import path
from customer.views import *




urlpatterns = [

   path('api/update_profile/<int:id>/', update_profile, name='update_profile'),
   path('api/add_address/<customer_id>/',add_shipping_address),
   path('api/edit_address/<address_id>/', edit_shipping_address),
   path('api/delete_address/<address_id>/', delete_shipping_address),
   path('api/get_address_by_id/<address_id>/',get_shipping_address),
   path('api/get_all_address/<customer_id>/',get_all_shipping_addresses),
   path('api/get_all_customers/',get_all_customers),
   path('api/get_customer/<id>',get_customer_by_id),



]