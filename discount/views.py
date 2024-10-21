from django.shortcuts import render
from .modules import *

# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_discount(request):
    try:
        payload = request.data
        payload['user'] = request.user.id  # Add the current user to the payload
        data_serializer = DiscountSerializer(data=payload, context={'request': request})

        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Discount added successfully",
                'data': data_serializer.data,
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "Invalid data",
                'errors': data_serializer.errors,
            })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })







@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_discount(request, id):
    try:
        discountObj = Discount.objects.get(id=id)
        data = request.data

        # Handle Many-to-Many fields separately
        included_products = data.pop('included_products', None)
        excluded_products = data.pop('excluded_products', None)
        included_categories = data.pop('included_categories', None)
        excluded_categories = data.pop('excluded_categories', None)

        # Partial update for other fields
        serializer = DiscountSerializer(discountObj, data=data, partial=True, context={'request': request})

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Something Went Wrong'
            })

        serializer.save()

        # Handle updating Many-to-Many fields
        if included_products is not None:
            discountObj.included_products.set(included_products)  # Update included_products
        if excluded_products is not None:
            discountObj.excluded_products.set(excluded_products)  # Update excluded_products
        if included_categories is not None:
            discountObj.included_categories.set(included_categories)  # Update included_categories
        if excluded_categories is not None:
            discountObj.excluded_categories.set(excluded_categories)  # Update excluded_categories

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': "Discount updated successfully"
        })

    except Discount.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Discount not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@permission_classes([IsAuthenticated])

def all_discount(request):
    try:
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts,many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message':'Get All Discount Fetched Successfully',
            'data':serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_discount_by_id(request, id):
    try:
        discount = Discount.objects.get(id=id)
        data_serializer = DiscountSerializer(discount, many=False)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })

    except Discount.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Discount not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_discount(request,id):
    try:
        discountObj = Discount.objects.get(id=id)
        discountObj.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Discount Deleted Successfully!',
            'discount_id': id
        },status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })