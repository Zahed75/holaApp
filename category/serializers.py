from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','user', 'categoryName', 'parentCategory', 'coverImage', 'slug']
        read_only_fields = ['id', 'slug']  

    def create(self, validated_data):
        # Add any custom creation logic here if necessary
        return super().create(validated_data)
