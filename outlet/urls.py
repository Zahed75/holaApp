from django.urls import path
from outlet.views import *





urlpatterns = [
 
  path('api/create-outlet',createOutlet),
  path('api/update-outlet/<id>',updateOutlet),

]