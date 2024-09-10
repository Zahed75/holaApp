from django.db import models
from django.contrib.auth.models import User
from category.models import *
from products.models import *
from django.core.validators import MinValueValidator

# Create your models here.


class Discount(models.Model):
    # General Section
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discounts')
    code = models.CharField(max_length=50, unique=True, help_text="Enter the coupon code.")
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discount amount")
    allow_free_shipping = models.BooleanField(default=False, help_text="Allow free shipping?")
    coupon_expiry = models.DateField(null=True, blank=True, help_text="Expiry date of the coupon")

    # Usage Restrictions Section
    minimum_spend = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        null=True, blank=True, help_text="Minimum spend to apply coupon"
    )
    maximum_spend = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        null=True, blank=True, help_text="Maximum spend to apply coupon"
    )
    individual_use_only = models.BooleanField(default=False, help_text="If true, coupon cannot be used with other coupons.")
    exclude_sale_items = models.BooleanField(default=False, help_text="Exclude items on sale?")
    excluded_products = models.ManyToManyField('products.Product', blank=True, help_text="Products excluded from coupon usage")
    included_categories = models.ManyToManyField('category.Category', related_name='included_discounts', blank=True, help_text="Categories to include")
    excluded_categories = models.ManyToManyField('category.Category', related_name='excluded_discounts', blank=True, help_text="Categories to exclude")
    blocked_accounts = models.ManyToManyField(User, blank=True, help_text="Users who cannot use this coupon")

    # Usage Limits Section
    usage_limit_per_coupon = models.PositiveIntegerField(null=True, blank=True, help_text="Max number of times this coupon can be used in total")
    usage_limit_per_user = models.PositiveIntegerField(null=True, blank=True, help_text="Max number of times a user can use this coupon")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

