from .modules import *
# Create your views here.



@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])

def create_product(request):
    try:
        payload = request.data
        payload['user']= request.user.id

        data_serializer = ProductSerializer(data=payload, context={'request': request})

        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Product added successfully",
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
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_inventory(request, id):
    try:
        # Fetch the product using the provided ID
        product = Product.objects.get(id=id)
        
        # Update the payload with the product reference
        payload = request.data.copy()
        payload['product'] = product.id

        data_serializer = InventorySerializer(data=payload, context={'request': request})
        
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Inventory added successfully",
                'data': data_serializer.data,
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "Invalid data",
                'errors': data_serializer.errors,
            })
    
    except Product.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': "Product not found"
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['PUT'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def update_product(request,id):

    try:
        productObj = Product.objects.get(id=id)
        
        serializer = ProductSerializer(productObj,data=request.data,partial=True,context={'request':request})
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors, 
                'message': 'Something Went Wrong'
            })
        serializer.save()
        print(serializer)
        return Response({
            'status': 200, 
            'payload': serializer.data,
            'message': "Product updated successfully"
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
    





@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_inventory(request,id):

    try:
        inventory = Inventory.objects.get(id=id)
        serializers = InventorySerializer(inventory,data=request.data,partial=True,context={'request':request})
        if not serializers.is_valid():
            serializers.save()
            return Response({
                 'status': 400,
                'payload': serializers.errors, 
                'message': 'Something Went Wrong'
            })
        serializers.save()
        return Response({
            'status': 200, 
            'payload': serializers.data,
            'message': "Inventroy updated successfully"
        })
    except Exception as e:
         return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_product(request,id):
    try:
        prodcutObj = Product.objects.get(id=id)
        prodcutObj.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product Deleted Successfully!',
            'category_id': id 
        },status=status.HTTP_200_OK)
    
    except Product.DoesNotExist:
         return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Product not found!'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
           return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def inventory_delete(request,id):
    try:
        inventoryObjects = Inventory.objects.get(id=id)
        inventoryObjects.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Inventory Deleted Successfully!',
            'category_id': id 
        },status=status.HTTP_200_OK)
    
    
    except Exception as e:
            return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    try:
        products = Product.objects.all()
        data_serializer = ProductSerializer(products,many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message':'Get All Products Fetched Successfully',
            'data':data_serializer.data
        })
    except Exception as e:
          return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_products_by_id(request,id):
    try:
        products = Product.objects.get(id=id)
        data_serializer = ProductSerializer(products,many=False)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })
    
    except Exception as e:
         return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
        
