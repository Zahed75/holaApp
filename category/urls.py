from django.urls import path
from category.views import *





urlpatterns = [
 
    path('api/addCategory',add_Category),
    path('api/editCategory/<id>',updateCategory),
    path('api/delete-category/<id>',deleteCategory),
    path('api/get-CategoryList',get_allCategory),
    path('api/getCategoryByName/<str:categoryName>',getCategoryById),
    path('api/getCategoryById/<id>',getCategoryById)

]