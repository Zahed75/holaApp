# Generated by Django 5.1 on 2024-09-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0008_alter_userprofile_otp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='unique_user_id',
            field=models.CharField(default=1, editable=False, max_length=36, unique=True),
            preserve_default=False,
        ),
    ]