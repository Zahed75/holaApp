# Generated by Django 5.1 on 2024-09-17 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_customer_club_points_alter_customer_user'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shippingAddress',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.shippingaddress'),
            preserve_default=False,
        ),
    ]