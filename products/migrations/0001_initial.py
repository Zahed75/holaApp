# Generated by Django 5.1 on 2024-09-30 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=322, verbose_name='Product Name')),
                ('productDescription', models.TextField(max_length=10000, verbose_name='Descriptions')),
                ('seoTitle', models.CharField(max_length=400, verbose_name='SEO Title')),
                ('seoDescription', models.TextField(max_length=700)),
                ('productShortDescription', models.TextField(max_length=5000)),
                ('color', models.CharField(max_length=100, verbose_name='Color')),
                ('regularPrice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Regular Price')),
                ('salePrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Sale Price')),
                ('saleStart', models.DateTimeField(blank=True, null=True, verbose_name='Sale Start')),
                ('saleEnd', models.DateTimeField(blank=True, null=True, verbose_name='Sale End')),
                ('sizeCharts', models.ImageField(blank=True, null=True, upload_to='size_charts', verbose_name='Size Charts')),
                ('fabric', models.CharField(max_length=200, verbose_name='Fabric')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Weight (kg)')),
                ('dimension_length', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Length (cm)')),
                ('dimension_width', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Width (cm)')),
                ('dimension_height', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Height (cm)')),
                ('featureImage', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Feature Image')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='products', to='category.category')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50, verbose_name='Size')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('barCode', models.CharField(max_length=100, unique=True, verbose_name='Bar Code')),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(choices=[('gallery', 'Gallery Image')], default='gallery', max_length=20)),
                ('image', models.ImageField(upload_to='products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
    ]
