from django.urls import path
from discount.views import *




urlpatterns = [
    path('api/addDiscount',add_discount),
    path('api/updateDiscount/<id>',edit_discount),
    path('api/getAllDiscount',all_discount),
    path('api/get_discount/<id>',get_discount_by_id),
    path('api/delete_discount/<id>',delete_discount),

]