from django.contrib import admin
from.models import *
# Register your models here.


@admin.register(Discount)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id','coupon_amount','coupon_expiry','minimum_spend','maximum_spend','usage_limit_per_user')
