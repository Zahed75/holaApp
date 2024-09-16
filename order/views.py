from.modules import *
# Create your views here.






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Generate a unique order ID
    order_id = get_random_string(length=10).upper()

    data = {
        'orderId': order_id,
        'amount': request.data.get('amount'),
        'origin': request.data.get('origin'),
        'orderStatus': request.data.get('orderStatus', 'Pending Payment'),
        'status': request.data.get('status', True)
    }

    # Manually add customer details
    data['customer'] = user_profile.id
    data['customerName'] = user_profile.user.username  # Using username as the name
    data['customerPhoneNumber'] = user_profile.phone_number

    serializer = OrderSerializer(data=data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

