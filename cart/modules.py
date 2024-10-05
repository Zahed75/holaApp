from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from products.models import Product

from .serializers import CartSerializer
from rest_framework.views import APIView

from customer.models import *