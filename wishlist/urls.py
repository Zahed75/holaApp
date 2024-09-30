from django.urls import path
from .views import *





urlpatterns = [
    path('api/create_wishlist/', create_wishlist),
    path('api/update_wishlist/<int:id>/', update_wishlist),
    path('api/delete_wishlist/<int:id>/', delete_wishlist),
    path('api/get_wishlist/<int:user_id>/', get_wishlist),

]
