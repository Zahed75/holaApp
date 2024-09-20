from django.urls import path
from products.views import *





urlpatterns = [

    path('api/addProduct',create_product),
    path('api/addInventoryByProductId/<id>',add_inventory),
    path('api/editProduct/<id>',update_product),
    path('api/editInventoryByProductId/<id>',update_inventory),
    path('api/deleteProduct/<id>',delete_product),
    path('api/deleteInventoryByProductId/<id>',inventory_delete),
    path('api/get-allProducts',get_products),
    path('api/get-products/<id>',get_products_by_id),
    path('api/inventory/<int:product_id>/', get_inventory_by_product)
 
]