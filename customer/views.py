from.modules import *
# Create your views here.




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request, id):
    try:
        # Fetch the UserProfile instance
        user_profile = Customer.objects.get(id=id)
        user = user_profile.user

        # Fetch the Customer instance associated with the UserProfile
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return Response({
                'status': 404,
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)

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

    except Exception as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)








# Add Shipping Address
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_shipping_address(request, customer_id):
    try:
        # Fetch the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Serialize the request data (Address details)
        serializer = ShippingAddressSerializer(data=request.data)

        # Validate the data
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Validation Error'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save the shipping address for the customer
        serializer.save(customer=customer)

        return Response({
            'status': 201,
            'payload': serializer.data,
            'message': 'Shipping address added successfully'
        }, status=status.HTTP_201_CREATED)

    except Customer.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Customer not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)







# Edit Shipping Address
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_shipping_address(request, address_id):
    try:
        # Fetch the shipping address by ID
        address = ShippingAddress.objects.get(id=address_id)

        # Serialize and validate the request data
        serializer = ShippingAddressSerializer(address, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Validation Error'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated address data
        serializer.save()

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': 'Shipping address updated successfully'
        }, status=status.HTTP_200_OK)

    except ShippingAddress.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Address not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Delete Shipping Address
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_shipping_address(request, address_id):
    try:
        # Fetch the shipping address by ID
        address = ShippingAddress.objects.get(id=address_id)

        # Delete the shipping address
        address.delete()

        return Response({
            'status': 200,
            'message': 'Shipping address deleted successfully'
        }, status=status.HTTP_200_OK)

    except ShippingAddress.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Address not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Get Shipping Address
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shipping_address(request, address_id):
    try:
        # Fetch the shipping address by ID
        address = ShippingAddress.objects.get(id=address_id)

        # Serialize the shipping address
        serializer = ShippingAddressSerializer(address)

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': 'Shipping address retrieved successfully'
        }, status=status.HTTP_200_OK)

    except ShippingAddress.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Address not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Get All Shipping Addresses
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_shipping_addresses(request, customer_id):
    try:
        # Fetch the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Fetch all shipping addresses related to the customer
        addresses = ShippingAddress.objects.filter(customer=customer)

        # Serialize the list of shipping addresses
        serializer = ShippingAddressSerializer(addresses, many=True)

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': 'Shipping addresses retrieved successfully'
        }, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Customer not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'status': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def get_all_customers(request):
    try:
        customers = Customer.objects.all()  # Fetch all customers
        serializer = CustomerSerializer(customers, many=True)

        return Response({
            'code': status.HTTP_200_OK,
            'message': "All customers fetched successfully",
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_customer_by_id(request,id):
    try:
     customers=Customer.objects.get(id=id)
     data_serializer = CustomerSerializer(customers)
     return Response({
         'code': status.HTTP_200_OK,
         'message': 'Customer Get Successfully',
         'data': data_serializer.data
     })

    except Customer.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Customer not found'
        },status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


