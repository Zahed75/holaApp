from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.models import User
from products.models import *

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wishlist.models import *
