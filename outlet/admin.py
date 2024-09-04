from django.contrib import admin
from .models import *

from unfold.admin import ModelAdmin as unfoldModelAdmin



class OutletAdmin(unfoldModelAdmin):
    list_display = ('id', 'manager', 'location')

admin.site.register(Outlet, OutletAdmin)
