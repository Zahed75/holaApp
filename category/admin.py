from django.contrib import admin
from .models import Category

from unfold.admin import ModelAdmin as unfoldModelAdmin

class CategoryModelAdmin(unfoldModelAdmin):
    list_display = ('id','slug','categoryName', 'parentCategory', 'coverImage')  

    prepopulated_fields = {"slug": ("categoryName",)} 

    search_fields = ('categoryName', 'slug') 

    list_filter = ('parentCategory',) 




admin.site.register(Category, CategoryModelAdmin)

