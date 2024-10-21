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

def edit_discount(request,id):
    try:
        discountObj = Discount.objects.get(id=id)
        serializer = DiscountSerializer(discountObj,data=request.data,partial=True,context={'request':request})

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Something Went Wrong'
            })
        serializer.save()
        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': "Discount updated successfully"
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })



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