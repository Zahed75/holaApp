from django.contrib import admin
from .models import Category

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id','slug','categoryName', 'parentCategory', 'coverImage')  

    prepopulated_fields = {"slug": ("categoryName",)} 

    search_fields = ('categoryName', 'slug') 

    list_filter = ('parentCategory',) 




admin.site.register(Category, CategoryModelAdmin)

