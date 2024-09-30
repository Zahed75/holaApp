from django.urls import path
from .views import *





urlpatterns = [
    path('api/create_wishlist/', create_wishlist),
    path('api/wishlist/<int:id>/', update_wishlist),
    path('api/wishlist/<int:id>/', delete_wishlist),
]
