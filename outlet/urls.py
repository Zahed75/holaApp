from django.urls import path
from outlet.views import *





urlpatterns = [
 
  path('api/create-outlet',createOutlet),
  path('api/update-outlet/<id>',updateOutlet),
  path('api/get-all-outlets/',getAllOutlets),
  path('api/get-outlet/<id>',getOutletById),
  path('api/delete-outlet/<id>',deleteOutlet)
]