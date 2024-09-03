from django.contrib import admin
from .models import *





class OutletAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager', 'location')

admin.site.register(Outlet, OutletAdmin)
