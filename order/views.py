from.modules import *



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    customer_id = data.get('customer_id')
    if not customer_id:
        return Response({
            "status": 400,
            "message": "Customer ID is required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        customer = Customer.objects.get(id=customer_id, user=user)
    except Customer.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Invalid customer. Please provide a valid customer ID for the logged-in user."
        }, status=status.HTTP_400_BAD_REQUEST)

    shipping_address = customer.shipping_addresses.first()  # Assuming we use the first shipping address
    if not shipping_address:
        return Response({
            "status": 400,
            "message": "No shipping address found for this customer."
        }, status=status.HTTP_400_BAD_REQUEST)

    order_items_data = data.get('order_items')
    if not order_items_data:
        return Response({
            "status": 400,
            "message": "Order items are required."
        }, status=status.HTTP_400_BAD_REQUEST)
    order_data = {
        "user": user.id,
        "status": data.get('status', 'pending'),
        "shippingAddress": shipping_address.id,
        "shipping_cost": data.get('shipping_cost', 0),
        "order_items": [],

    }

    total_price = Decimal(0)
    order_items = []

    for item in order_items_data:
        product_id = item.get('product')
        quantity = item.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        price_per_item = product.salePrice if product.salePrice else product.regularPrice

        if price_per_item is None:
            return Response({
                "status": 400,
                "message": f"Product {product_id} does not have a valid price."
            }, status=status.HTTP_400_BAD_REQUEST)

        total_price += price_per_item * quantity


        order_items.append({
            'product': product_id,
            'quantity': quantity,
            'price': price_per_item
        })

    order_data['order_items'] = order_items

    try:

        serializer = OrderSerializer(data=order_data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()


            order.total_price = total_price
            order.vat = total_price * Decimal(0.05)
            order.grand_total = total_price + order.shipping_cost + order.vat
            order.save()

            return Response({
                "status": 201,
                "message": "Order placed successfully",
                "order": OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": 400,
            "message": "Failed to place order",
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
