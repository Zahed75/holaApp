from django.urls import path
from .views import dashboard_stats

urlpatterns = [
    path('api/stats-dashboard/', dashboard_stats, name='dashboard_stats'),
]


