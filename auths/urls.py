from django.urls import path
from auths.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView




urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register-phone/', register_user),
    path('api/verify-otp/',verify_otp),
    path('api/resendOtp/',resend_otp),
    path('api/tokenPair/',CustomTokenObtainPairView.as_view()),
    path('api/all-users/',all_users),


]