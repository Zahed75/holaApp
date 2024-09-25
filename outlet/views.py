from django.shortcuts import render
from .models import *
from .modules import *
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOutlet(request):
    try:
        # Serialize the data
        data_serializer = OutletSerializer(data=request.data, context={'request': request})

        if data_serializer.is_valid():
            # Save the outlet and return the response
            outlet = data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Outlet added successfully",
                'data': data_serializer.data,  # Return the serialized outlet data
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

def updateOutlet(request,id):
    try:
        outletObj = Outlet.objects.get(id=id)
        serializers = OutletSerializer(outletObj,data=request.data,partial=True,context={'request':request})
        if not serializers.is_valid():
            return Response({
                'status': 400,
                'payload': serializers.errors, 
                'message': 'Something Went Wrong'
            })
        serializers.save()
        return Response({
            'status': 200, 
            'payload': serializers.data,
            'message': "Outlet updated successfully"
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getAllOutlets(request):
    try:
        outlets = Outlet.objects.all()
        data_serializers = OutletSerializer(outlets,many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message':'Get All Products Fetched Successfully',
            'data':data_serializers.data
        })
    
    except Exception as e:
       return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
 



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOutletById(request, id):
    try:
        outlet = Outlet.objects.get(id=id)
        data_serializer = OutletSerializer(outlet, many=False)  # Use the updated serializer
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })
    
    except Outlet.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Outlet not found'
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def  deleteOutlet(request,id):
    try:
        OutletObj = Outlet.objects.get(id=id)
        OutletObj.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product Deleted Successfully!',
            'category_id': id 
        },status=status.HTTP_200_OK)
    
    except Outlet.DoesNotExist:
          return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Outlet not found!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })