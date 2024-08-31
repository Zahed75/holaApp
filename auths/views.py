
from .modules import *

API_KEY = 'dbf5ae53b49fdf65ac01f09ef7385686ac42ea4d'

@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP
            otp = str(random.randint(1000, 9999))

            # Send OTP via SMS
            message = f"Your OTP code is {otp}. Please use this to verify your account."
            response = send_sms(request.data.get('phone_number'), message, API_KEY)

            # Create UserProfile with the fixed role
            profile = UserProfile.objects.create(
                user=user,
                role=request.data.get('role'),
                phone_number=request.data.get('phone_number'),
                otp=otp,
                otp_created_at=timezone.now(),
                otp_verified=False  
            )

            return Response({
                'id': user.id,
                'role': profile.role,
                'phone_number': profile.phone_number,
                'otp': profile.otp,
                'is_verified': profile.otp_verified,
                'message': 'User registered successfully. OTP sent to the phone number.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
            # Mark OTP as verified
            profile.otp_verified = True
            profile.save()

            # Generate tokens
            refresh = RefreshToken.for_user(profile.user)
            return Response({
                'user': {
                    'id': profile.user.id,
                    'role': profile.role,
                    'phone_number': profile.phone_number,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            })
        else:
            return Response({'error': 'Invalid OTP or OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
