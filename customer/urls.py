from django.urls import path
from customer.views import *




urlpatterns = [

   path('api/update_profile/<int:id>/', update_profile, name='update_profile'),

]