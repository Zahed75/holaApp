# Generated by Django 5.1 on 2024-10-05 21:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_user_id', models.CharField(editable=False, max_length=36, unique=True)),
                ('role', models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin'), ('outlet_manager', 'Outlet Manager')], max_length=20)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('otp', models.CharField(max_length=4)),
                ('otp_created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
