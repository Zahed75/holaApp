from django.db import models
from auths.models import *
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categoriesList')
    categoryName = models.CharField(max_length=122,blank=False)
    parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    coverImage = models.ImageField(upload_to='categories', blank=True, null=True)
    slug = models.SlugField(unique=True) 

    def __str__(self):
        return self.categoryName