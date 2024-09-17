
from.modules import *
# Create your views here.





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request, id):
    try:
        # Fetch the UserProfile instance
        user_profile = UserProfile.objects.get(id=id)
        user = user_profile.user

        # Fetch or create the Customer instance associated with the UserProfile
        customer, created = Customer.objects.get_or_create(user=user)

        # Serialize the customer object with partial update
        serializer = CustomerSerializer(customer, data=request.data, partial=True, context={'request': request})

        # Check if the data is valid
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Validation Error'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save the changes to the customer
        serializer.save()

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': "Profile updated successfully"
        }, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'UserProfile not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Customer.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Customer not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
