from django.urls import path
from category.views import *





urlpatterns = [
 
    path('api/addCategory',add_Category),
    path('api/editCategory/<id>',updateCategory),
    path('api/delete-category/<id>',deleteCategory),
    path('api/get-CategoryList',get_allCategory),
    path('api/getCategoryByName/<str:categoryName>',get_category_by_name),
    path('api/getCategoryById/<id>',get_category_by_id),
    path('api/delete_categories/',delete_categories)

]