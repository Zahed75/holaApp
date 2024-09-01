from django.urls import path
from category.views import *





urlpatterns = [
 
    path('api/addCategory',add_Category),
    path('api/editCategory/<id>',updateCategory),

]