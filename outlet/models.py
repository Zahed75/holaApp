from django.db import models
from auths.models import *
from django.contrib.auth.models import User

# Create your models here.


class Outlet(models.Model):
    manager = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outlets')
    outletName = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=340,blank=True,null=True)
   
    def __str__(self):
        return self.outletName