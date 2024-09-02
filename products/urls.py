from django.urls import path
from products.views import *





urlpatterns = [

    path('api/addProduct',createProduct),
    path('api/addInventoryByProductId/<id>',addInventory)

 
]