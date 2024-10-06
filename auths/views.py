from customer.models import Customer
from .modules import *




@api_view(['POST'])
def register_user(request):
    try:
        role = request.data.get('role')
        if role not in dict(UserProfile.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        required_fields = ['phone_number']

        if role == 'outlet_manager':
            required_fields += ['first_name', 'last_name', 'email']

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
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=request.data.get('phone_number'),
                email=f'{request.data.get("phone_number")}@example.com',  # Dummy email
                first_name='',
                last_name=''
            )

        # Ensure the user ID is properly assigned
        if not user.id:
            user.save()

        # Generate OTP
        otp = str(random.randint(1000, 9999))

        # Send OTP via SMS
        message = f"Your OTP code is {otp}. Please use this to verify your account."
        response = send_sms(request.data.get('phone_number'), message)

        # Create a UserProfile with the provided role
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=request.data.get('phone_number'),
            otp=otp,
            otp_created_at=timezone.now()
        )
        profile.save()

        # Create a Customer instance
        customer = Customer.objects.create(
            user=user,
            name=request.data.get('first_name', '') + ' ' + request.data.get('last_name', ''),
            email=request.data.get('email', f'{request.data.get("phone_number")}@example.com'),  # Dummy email for customers
            dob=request.data.get('dob'),  # Assuming you're collecting date of birth for customers
        )

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
        # Fetch the UserProfile based on the phone number
        profile = UserProfile.objects.get(phone_number=phone_number)

        # Validate the OTP
        if profile.is_otp_valid(otp):
            profile.otp_verified = True
            profile.save()

            # Fetch the associated user and customer
            user = profile.user
            customer = Customer.objects.get(user=user)  # Fetch the customer linked to this user

            # Generate tokens using Simple JWT
            refresh = RefreshToken.for_user(user)

            # Serialize the user and customer data
            user_serializer = UserSerializer(user)
            customer_serializer = CustomerSerializer(customer)

            # Serialize the wishlist data and add it to the customer data
            wishlist_serializer = WishlistSerializer(customer.wishlists.all(), many=True)

            # Add the wishlist to the customer data
            customer_data = customer_serializer.data
            customer_data['wishlist'] = wishlist_serializer.data  # Embed wishlist in customer data

            # Return the response with access token, user info, and customer info (with wishlist included)
            return Response({
                'user': {
                    'id': user.id,  # Return correct user ID
                    'unique_id': profile.unique_user_id,  # Return the unique user ID from profile
                    'role': profile.role,  # Return the user role
                    'phone_number': profile.phone_number,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'customer': customer_data
                },
                 # Customer info with embedded wishlist
            })
        else:
            return Response({'error': 'Invalid OTP or OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found for this user'}, status=status.HTTP_404_NOT_FOUND)

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
        response = send_sms(request.data.get('phone_number'), message)

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
            send_sms(phone_number, message)  # No need to pass the API key manually

            return Response({
                "code": status.HTTP_200_OK,
                "message": "OTP sent successfully. Please verify to continue.",
                "otp": otp
            })

        except UserProfile.DoesNotExist:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "User with this phone number does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def all_users(request):
    try:

        all_users = User.objects.exclude(id__in=Customer.objects.values('user_id'))

        # Serialize the filtered list of users
        data_serializer = UserSerializer(all_users, many=True, context={'request': request})

        return Response({
            'code': status.HTTP_200_OK,
            'message': "All Users Fetched Successfully",
            'data': data_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
