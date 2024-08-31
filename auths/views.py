from django.shortcuts import render
from builtins import Exception
from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken, Token
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, logout
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.



@api_view(['POST'])

def home(request):
    return Response({
        "status":200,
        "Response":"Hello Im Back"
    })

