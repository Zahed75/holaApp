from django.shortcuts import render
from .modules import *
# Create your views here.




@api_view(['POST'])
@parser_classes([MultiPartParser])

def add_Category(request):
    try:
        payload = request.data

        data_serializer = CategorySerializer(data=payload,context={'request':request})
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code':status.HTTP_200_OK,
                'message':"Category added successfully",
                'data':data_serializer.data,
            })

    except Exception as e:
        return Response({
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        })