from .modules import *
# Create your views here.



@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])

def createProduct(request):
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
def addInventory(request, id):
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
