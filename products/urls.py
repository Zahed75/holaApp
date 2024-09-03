from django.urls import path
from products.views import *





urlpatterns = [

    path('api/addProduct',createProduct),
    path('api/addInventoryByProductId/<id>',addInventory),
    path('api/editProduct/<id>',updateProduct),
    path('api/editInventoryByProductId/<id>',updateInventory),
    path('api/deleteProduct/<id>',deleteProduct),
    path('api/deleteInventoryByProductId/<id>',InventoryDelete),
    path('api/get-allProducts',getProducts),
 
]