from.modules import *
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        payload = request.data.copy()
        order_items_data = payload.pop('order_items', [])
        total_amount = sum(Product.objects.get(id=item['product']).regularPrice * item.get('quantity', 1)
                           for item in order_items_data)

        payload['amount'] = total_amount
        payload['customer'] = request.user.userprofile.id

        order_serializer = OrderSerializer(data=payload, context={'request': request})

        if order_serializer.is_valid():
            order = order_serializer.save()

            # Save order items
            for item in order_items_data:
                item['order'] = order.id  # Link order to each item
                item_serializer = OrderItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': "Invalid order item data",
                                     'errors': item_serializer.errors})

            return Response({'code': status.HTTP_201_CREATED, 'message': "Order created successfully",
                             'data': order_serializer.data})
        else:
            return Response(
                {'code': status.HTTP_400_BAD_REQUEST, 'message': "Invalid data", 'errors': order_serializer.errors})

    except Product.DoesNotExist:
        return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': "Product not found"})
    except Exception as e:
        return Response({'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})
