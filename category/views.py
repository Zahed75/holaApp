from django.shortcuts import render
from .modules import *
# Create your views here.





@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def add_Category(request):
    try:
        payload = request.data
        payload['user'] = request.user.id
        # Serialize the data
        data_serializer = CategorySerializer(data=payload, context={'request': request})
        
        # Validate and save the data
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Category added successfully",
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
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def updateCategory(request, id):  # Add id as a parameter
    try:
        catObj = Category.objects.get(id=id)
        serializer = CategorySerializer(catObj, data=request.data, partial=True, context={'request': request})  # Correct context passing
        if not serializer.is_valid():
            return Response({'status': 400, 'payload': serializer.errors, 'message': 'Something Went Wrong'})  # Return errors instead of data on failure
        serializer.save()
        return Response({'status': 200, 'payload': serializer.data, 'message': "Category updated successfully"})
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
