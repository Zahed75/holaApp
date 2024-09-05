from django.shortcuts import render
from .models import *
from .modules import *
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])

def createOutlet(request):
    try:
        # Ensure the manager (current user) is added to the payload
        payload = request.data.copy()  # Copy the request data to avoid modifying the original data
        payload['manager'] = request.user.id  # Set the manager to the current authenticated user

        # Serialize the data
        data_serializer = OutletSerializer(data=payload, context={'request': request})
        if data_serializer.is_valid():
            # Save the data
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Outlet added successfully",
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


