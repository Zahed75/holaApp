from rest_framework import serializers
from category.models import Category
from products.models import Product
from products.serializers import *
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['categoryName', 'id', 'user', 'parentCategory', 'slug', 'products']
        read_only_fields = ['id', 'slug']

    def get_products(self, obj):
        # Import ProductSerializer here to avoid circular import
        from products.serializers import ProductSerializer
        products = Product.objects.filter(category=obj)
        return ProductSerializer(products, many=True, context=self.context).data
