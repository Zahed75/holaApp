from django.db import models
from category.models import *
from django.contrib.auth.models import User

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    productName = models.CharField(max_length=322, verbose_name='Product Name')
    featureImage = models.ImageField(upload_to='features')
    productsGallery = models.ImageField(upload_to='gallery')
    productDescription = models.TextField(max_length=10000, verbose_name='Descriptions')
    seoTitle = models.CharField(max_length=400, verbose_name='SEO Title')
    seoDescription = models.TextField(max_length=700)
    productShortDescription = models.TextField(max_length=5000)

    # General Section
    regularPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Regular Price')
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sale Price', null=True, blank=True)
    saleStart = models.DateTimeField(verbose_name='Sale Start', null=True, blank=True)
    saleEnd = models.DateTimeField(verbose_name='Sale End', null=True, blank=True)

    # Inventory Section
    sizeCharts = models.ImageField(upload_to='size_charts', null=True, blank=True, verbose_name='Size Charts')
    fabric = models.CharField(max_length=200, verbose_name='Fabric')

    # Shipping Section
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimension_length = models.DecimalField(max_digits=12,verbose_name='Length (cm)')
    dimension_width = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Width (cm)')
    dimension_height = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Height (cm)')

    def __str__(self):
        return self.productName

class Inventory(models.Model):
    product = models.ForeignKey(Product, related_name='inventory', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, verbose_name='Size')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    barCode = models.CharField(max_length=100, unique=True, verbose_name='Bar Code')
    available = models.BooleanField(default=True, verbose_name='Available')

    def __str__(self):
        return f'{self.product.productName} - {self.size}'
