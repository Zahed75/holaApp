from .modules import *
from.serializers import *
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wishlist(request):
    try:
        # Create a new wishlist item but set the user from the request
        serializer = WishlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Save the wishlist items
            wishlist_items = serializer.save()
            return Response({
                'code': status.HTTP_201_CREATED,
                'message': "Wishlist Created Successfully",
                'data': WishlistSerializer(wishlist_items, many=True).data  # Serialize the list of wishlist items
            })
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': "Validation Error",
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




# Update Wishlist (e.g., add a product)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_wishlist(request, id):
    try:
        wishlist_item = Wishlist.objects.get(id=id)
        serializer = WishlistSerializer(wishlist_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Wishlist.DoesNotExist:
        return Response({'message': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)






# Delete Wishlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_wishlist(request, id):
    try:
        wishlist_item = Wishlist.objects.get(id=id)
        wishlist_item.delete()
        return Response({'message': 'Wishlist item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'message': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)
