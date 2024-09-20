from .modules import *
from auths.models import User

API_KEY = '3cbe6feb4dc1d795ce934790b238727b013f542a'

@api_view(['POST'])
def register_user(request):
    try:
      
        role = request.data.get('role')
        if role not in dict(UserProfile.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        if role == 'outlet_manager':
      
            required_fields = ['first_name', 'last_name', 'email', 'phone_number']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            user = User.objects.create_user(
                username=request.data.get('email'),
                email=request.data.get('email'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name')
            )
        else:
 
            if not request.data.get('phone_number'):
                return Response({'error': 'Missing field: phone_number'}, status=status.HTTP_400_BAD_REQUEST)

      
            user = User.objects.create_user(
                username=request.data.get('phone_number'),
                email=f'{request.data.get("phone_number")}@example.com',  # Dummy email
                first_name='',  
                last_name=''   
            )

        # Generate OTP
        otp = str(random.randint(1000, 9999))

        # Send OTP via SMS
        message = f"Your OTP code is {otp}. Please use this to verify your account."
        response = send_sms(request.data.get('phone_number'), message, API_KEY)

        # Create a UserProfile with the provided role
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=request.data.get('phone_number'),
            otp=otp,
            otp_created_at=timezone.now()
        )
        profile.save()

        return Response({
            'id': profile.unique_user_id,  # Return the unique user ID here
            'role': profile.role,
            'phone_number': profile.phone_number,
            'otp': profile.otp,
            'is_verified': profile.otp_verified,
            'message': 'User registered successfully. OTP sent to the phone number.'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })









@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')

    try:
        profile = UserProfile.objects.get(phone_number=phone_number)
        if profile.is_otp_valid(otp):
            profile.otp_verified = True
            profile.save()

            # Generate tokens
            refresh = RefreshToken.for_user(profile.user)
            return Response({
                'user': {
                    'id': profile.unique_user_id,
                    'role': profile.role,
                    'phone_number': profile.phone_number,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            })
        else:
            return Response({'error': 'Invalid OTP or OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })
    




    
        
@api_view(['POST'])
def resend_otp(request):
    phone_number = request.data.get('phone_number')
    
    try:
        profile = UserProfile.objects.get(phone_number=phone_number)
        
        # Generate new OTP
        otp = str(random.randint(1000, 9999))
        
        # Send OTP via SMS
        message = f"Your new OTP code is {otp}. Please use this to verify your account."
        response = send_sms(phone_number, message, API_KEY)
        
        # Update OTP and OTP creation time
        profile.otp = otp
        profile.otp_created_at = timezone.now()
        profile.otp_verified = False
        profile.save()
        
        return Response({
            'phone_number': profile.phone_number,
            'otp': otp,  # Optionally include the new OTP in the response
            'message': 'New OTP sent to the phone number.'
        }, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
def tokenRefresh(request):
    try:
        payload = request.data
        refresh = RefreshToken(token=payload.get('refresh_token'), verify=True)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': str(refresh.payload['token_type']),
            'expiry': refresh.payload['exp'],
            'user_id': refresh.payload['user_id']
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
def tokenVerify(request):
    try:
        payload = request.data
        verify = UntypedToken(token=payload.get('access_token'))

        return Response({
            'access_token': str(verify.token),
            'token_type': str(verify.payload['token_type']),
            'expiry': verify.payload['exp'],
            'user_id': verify.payload['user_id'],
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })



API_KEY = 'dbf5ae53b49fdf65ac01f09ef7385686ac42ea4d'
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,) 

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            # Check if the user with the phone number exists
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            user = user_profile.user

            # Generate a 4-digit OTP
            otp = str(random.randint(1000, 9999))
            user_profile.otp = otp
            user_profile.otp_created_at = timezone.now()
            user_profile.save()

            # Send OTP via SMS
            message = f"Your OTP is {otp}. It is valid for 5 minutes."
            send_sms(phone_number, message, api_key=API_KEY,)

            return Response({
                "code": status.HTTP_200_OK,
                "message": "OTP sent successfully. Please verify to continue.",
                "otp":otp
            })

        except UserProfile.DoesNotExist:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "User with this phone number does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def all_users(request):
    try:
        all_users = User.objects.all()
        data_serializer = UserSerializer(all_users, many=True,context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': "Get All Users Fetched",
            'data': data_serializer.data
        })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "User with this phone number does not exist."
        }, status=status.HTTP_400_BAD_REQUEST)

