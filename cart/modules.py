from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from products.models import Product

from .serializers import CartSerializer
from rest_framework.views import APIView
from django.db.models import Sum
from customer.models import *
from discount.models import *
from auths.models import UserProfile
from order.modules import *