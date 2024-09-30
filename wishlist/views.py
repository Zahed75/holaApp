from .modules import *
from.serializers import *

# Create your views here.



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from wishlist.models import Wishlist
from .serializers import WishlistSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wishlist(request):
    try:
        serializer = WishlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            wishlist_items = serializer.save()
            return Response({
                'code': status.HTTP_201_CREATED,
                'message': "Wishlist Created Successfully",
                'data': wishlist_items  # Return serialized wishlist items
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





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_wishlist(request, id):
    try:
        wishlist_item = Wishlist.objects.get(id=id)

        # If the request contains product data, update the product
        if 'product' in request.data:
            product_id = request.data['product']
            product = Product.objects.get(id=product_id)  # Get the product based on the provided ID
            wishlist_item.product = product  # Update the wishlist item's product

        serializer = WishlistSerializer(wishlist_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save changes to the wishlist item
            # Include product information in the response
            updated_wishlist_item = Wishlist.objects.get(id=wishlist_item.id)
            response_data = {
                'id': updated_wishlist_item.id,
                'user': updated_wishlist_item.user.id,
                'product': ProductSerializer(updated_wishlist_item.product).data,  # Serialize product details
                'created_at': updated_wishlist_item.created_at
            }
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Wishlist.DoesNotExist:
        return Response({'message': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)





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


# views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request, user_id):
    try:
        # Fetch all wishlist items for the specified user
        wishlist_items = Wishlist.objects.filter(user__id=user_id)

        if not wishlist_items.exists():
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'No wishlist items found for this user'
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize the wishlist items and their associated products
        wishlist_data = []
        for item in wishlist_items:
            wishlist_data.append({
                'id': item.id,
                'user': item.user.id,
                'product': ProductSerializer(item.product).data,  # Include product details
                'created_at': item.created_at
            })

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Wishlist fetched successfully',
            'data': wishlist_data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
