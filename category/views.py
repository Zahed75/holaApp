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
            return Response({
                'status': 400,
                'payload': serializer.errors, 
                'message': 'Something Went Wrong'
                })  # Return errors instead of data on failure
        
        serializer.save()
        return Response({
            'status': 200, 
            'payload': serializer.data,
            'message': "Category updated successfully"
            })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCategory(request, id):
    try:
        catObj = Category.objects.get(id=id)
        catObj.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Category Deleted Successfully!',
            'category_id': id 
        }, status=status.HTTP_200_OK)
    
    except Category.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Category not found!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allCategory(request):
    try:
        listCategory = Category.objects.all()
        data_serializer =CategorySerializer(listCategory,many=True)
        return Response({
            'code':status.HTTP_200_OK,
            'message': "Get All Categories Fetched",
            'data':data_serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)

        },status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategoryById(request, categoryName):
    try:
        # Using get() to retrieve a single object by categoryName
        category = Category.objects.get(categoryName=categoryName)
        print("Check:", category)
        
        # Serializing the single object
        data_serializer = CategorySerializer(category, many=False)
        
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })
    
    except Category.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Category not found'
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getCategoryById(request,id):

    try:
        categorys = Category.objects.get(id=id)
        data_serializer = CategorySerializer(categorys,many=False)
        return Response({
              'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })
    
    except Category.DoesNotExist:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
    
    except Exception as e:
        return Response({
             'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        },status.HTTP_400_BAD_REQUEST)