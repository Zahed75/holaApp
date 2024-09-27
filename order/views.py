from .modules import *



@api_view(['POST'])
def create_order(request):
    try:
        user = request.user  # Get the user from the request
        shipping_address_id = request.data.get('shipping_address_id')
        coupon_code = request.data.get('coupon_code', None)
        items = request.data.get('items', [])
        shipping_cost = request.data.get('shipping_cost')  # Fetch shipping_cost from the request

        try:
            # Validate shipping address
            shipping_address = ShippingAddress.objects.get(id=shipping_address_id, customer__user=user)

            # Validate coupon code if provided
            coupon = None
            if coupon_code:
                coupon = Discount.objects.get(code=coupon_code)

            # Create the order
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                coupon_code=coupon,
                shipping_cost=Decimal(shipping_cost)  # Set the shipping cost from the request
            )

            # Create order items
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                # Use the salePrice if available, otherwise use regularPrice
                price_to_use = product.salePrice if product.salePrice else product.regularPrice

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=price_to_use
                )

            # Calculate totals (including VAT and grand total)
            order.calculate_totals()

            # Prepare response data
            order_details = {
                "order_id": order.id,
                "user": order.user.username,
                "shipping_address": {
                    "name": shipping_address.name,
                    "phone_number": shipping_address.phone_number,
                    "address": shipping_address.address,
                    "area": shipping_address.area,
                    "street": shipping_address.street,
                    "city": shipping_address.city,
                    "state": shipping_address.state,
                    "zip_code": shipping_address.zip_code,
                },
                "items": [
                    {
                        "product_id": item.product.id,
                        "product_name": item.product.productName,
                        "quantity": item.quantity,
                        "price": item.price,
                    } for item in order.order_items.all()
                ],
                "shipping_cost": str(order.shipping_cost),
                "total_price": str(order.total_price),
                "vat": str(order.vat),
                "grand_total": str(order.grand_total),
                "status": order.status,
                "created_at": order.created_at,
            }

            return Response({
                "message": "Order created successfully",
                "order_details": order_details
            }, status=status.HTTP_201_CREATED)

        except ShippingAddress.DoesNotExist:
            return Response({
                "code": 400,
                "message": "No shipping address found for this customer"
            }, status=status.HTTP_400_BAD_REQUEST)


        except Discount.DoesNotExist:
            return Response({
                "code": 400,
                "message": "Invalid coupon code"
            }, status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        return Response({
            "code": 500, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
