from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields ='__all__'


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = '__all__'