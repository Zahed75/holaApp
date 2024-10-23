from auths.models import UserProfile
from products.models import Inventory
from .modules import *
from sslcommerz_lib import SSLCOMMERZ




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        user = request.user
        shipping_address_id = request.data.get('shipping_address_id')
        payment_method = request.data.get('payment_method',
                                          'cash_on_delivery')  # Default to 'cash_on_delivery' if not provided
        coupon_code = request.data.get('coupon_code', None)
        items = request.data.get('items', [])
        shipping_cost = request.data.get('shipping_cost')

        # Retrieve the shipping address
        try:
            shipping_address = ShippingAddress.objects.get(id=shipping_address_id, customer__user=user)
        except ShippingAddress.DoesNotExist:
            return Response({
                "code": 400,
                "message": "No shipping address found for this customer"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the coupon if provided
        coupon = None
        use_regular_price = True  # Default to using regularPrice whether or not coupon is applied
        if coupon_code:
            try:
                coupon = Discount.objects.get(code=coupon_code)
            except Discount.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": "Invalid coupon code"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique order ID
        order_id = generate_unique_order_id()

        # Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            coupon_code=coupon,
            shipping_cost=Decimal(shipping_cost),
            payment_method=payment_method,
            order_id=order_id
        )

        total_price = 0  # To track the total price of all items

        # Loop through each item in the request to create OrderItem entries
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            size = item.get('size')
            color = item.get('color')

            try:
                product = Product.objects.get(id=product_id)
                inventory = Inventory.objects.get(product=product, size=size)

                if inventory.quantity < quantity:
                    return Response({
                        "code": 400,
                        "message": f"Not enough stock for {product.productName} in size {size}. Available: {inventory.quantity}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Always use regular price, regardless of coupon usage
                price_to_use = product.regularPrice

                # Calculate the total price of the order
                total_price += price_to_use * quantity

                # Create the order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price_to_use,
                    color=color
                )

                # Update inventory
                inventory.quantity -= quantity
                inventory.save()

            except Product.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Product with ID {product_id} does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)

            except Inventory.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Inventory for product {product.productName} and size {size} does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Apply discount if a coupon was used
        discount_amount = 0
        if coupon:
            discount_amount = coupon.coupon_amount
            total_price -= discount_amount

        # Calculate VAT (assuming 5% VAT rate)
        vat_rate = Decimal(0.05)
        vat_amount = total_price * vat_rate

        # Calculate grand total (total price + VAT + shipping cost)
        grand_total = total_price + vat_amount + Decimal(shipping_cost)

        # Update the order with totals
        order.total_price = total_price
        order.vat = vat_amount
        order.grand_total = grand_total
        order.save()

        # Prepare the order details response
        order_details = {
            "order_id": order.order_id,  # Return the custom order ID
            "user": order.user.username,
            "payment_method": order.payment_method,  # Return payment method
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
                    "size": item.size,
                    "color": item.color,
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

    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_unique_order_id():
    while True:
        random_number = random.randint(10000, 99999)
        order_id = f"HLG{random_number}"

        # Check if the order_id already exists
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    try:
        all_orders = Order.objects.all()
        data_serializer = OrderSerializer(all_orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message': data_serializer.data,
            'data': data_serializer.data
        })

    except Exception as e:
        return Response({
            "code": 500, "message": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )






@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request):
    try:
        order_id = request.data.get('order_id')  # This is the order_id in 'HLG#XXXXX' format
        new_status = request.data.get('new_status')

        # Validate input
        if not order_id or not new_status:
            return Response({'error': 'Order ID and new status are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the order exists using 'order_id' instead of 'id'
        try:
            order = Order.objects.get(order_id=order_id)  # Change here
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the order status
        order.status = new_status
        order.save()

        # Get the UserProfile associated with the user
        user_profile = UserProfile.objects.get(user=order.user)  # Access the UserProfile model to get phone_number
        phone_number = user_profile.phone_number

        # Prepare SMS content including order value and status
        message = (
            f"Dear Customer, your order ID {order.order_id} status has been updated to '{new_status}'. "
            f"Order Value: BDT {order.grand_total:.2f}. Thank you for shopping with us."
        )

        # Send SMS with order details
        response = send_sms(phone_number, message)

        # Return success response
        return Response({
            'order_id': order.order_id,  # Using 'order_id' field here
            'new_status': order.status,
            'message': 'Order status updated and SMS sent to the customer.'
        }, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({'error': 'UserProfile not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e),
            "errors": [{"message": str(e)}]
        }, status=status.status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_order_details(request, order_id):
    try:
        order_details = Order.objects.get(order_id=order_id)
        serializer = OrderSerializer(order_details)
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Order details retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except Order.DoesNotExist:

        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Order not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)






store_id = "holacombdlive"
store_pass = "5F5C5C6D2F7DC46431"
ssl_base_url = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# def initiate_payment(request, order_id):
#     try:
#         order = Order.objects.get(order_id=order_id, user=request.user)
#
#         if order.status != 'pending':
#             return Response({
#                 "status": "failed",
#                 "message": f"Order status is '{order.status}'. Only 'pending' orders can proceed to payment."
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         tran_id = str(uuid.uuid4())
#
#         post_data = {
#             'store_id': store_id,
#             'store_pass': store_pass,
#             'total_amount': str(order.grand_total),
#             'currency': "BDT",
#             'tran_id': tran_id,
#             'success_url': "http://localhost:3000/profile?screen=2&isPaymentSuccess=true",
#             'fail_url': "http://localhost:3000/payment?address=2&isPaymentSuccess=false",
#             'cancel_url': "http://localhost:3000/payment?address=2&isPaymentSuccess=false",
#             'cus_name': request.user.username,
#             'cus_email': request.user.email,
#             'cus_add1': order.shipping_address.address,
#             'cus_city': order.shipping_address.city,
#             'cus_country': "Bangladesh",
#             'cus_phone': order.shipping_address.phone_number,
#             'shipping_method': "NO",
#             'product_name': "Order Payment",
#             'product_category': "Ecommerce",
#             'product_profile': "general",
#         }
#
#         sslcz = SSLCOMMERZ({'store_id': store_id, 'store_pass': store_pass, 'issandbox': False})
#
#
#         response = sslcz.createSession(post_data)
#
#         if response['status'] == 'SUCCESS':
#             order.transaction_id = tran_id
#             order.status = 'processing'
#             order.save()
#
#
#             return Response({
#                 "status": "success",
#                 "payment_url": response['GatewayPageURL']
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "status": "failed",
#                 "message": "Payment initiation failed."
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#     except Order.DoesNotExist:
#         return Response({
#             "status": "failed",
#             "message": "Order not found."
#         }, status=status.HTTP_404_NOT_FOUND)
#
#     except Exception as e:
#         return Response({
#             "status": "failed",
#             "message": str(e)
#         }, status=status.HTTP_400_BAD_REQUEST)
#
#

def initiate_payment(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, user=request.user)

        if order.status != 'pending':
            return Response({
                "status": "failed",
                "message": f"Order status is '{order.status}'. Only 'pending' orders can proceed to payment."
            }, status=status.HTTP_400_BAD_REQUEST)

        tran_id = str(uuid.uuid4())

        # Dynamically pass the user ID in the success URL
        user_id = request.user.id
        success_url = f"http://localhost:3000/profile?screen=2&isPaymentSuccess=true&userId={user_id}"
        fail_url = "http://localhost:3000/payment?address=2&isPaymentSuccess=false"
        cancel_url = "http://localhost:3000/payment?address=2&isPaymentSuccess=false"

        post_data = {
            'store_id': store_id,
            'store_pass': store_pass,
            'total_amount': str(order.grand_total),
            'currency': "BDT",
            'tran_id': tran_id,
            'success_url': success_url,  # Update the success URL with the dynamic user ID
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_add1': order.shipping_address.address,
            'cus_city': order.shipping_address.city,
            'cus_country': "Bangladesh",
            'cus_phone': order.shipping_address.phone_number,
            'shipping_method': "NO",
            'product_name': "Order Payment",
            'product_category': "Ecommerce",
            'product_profile': "general",
        }

        sslcz = SSLCOMMERZ({'store_id': store_id, 'store_pass': store_pass, 'issandbox': False})

        response = sslcz.createSession(post_data)

        if response['status'] == 'SUCCESS':
            order.transaction_id = tran_id
            order.status = 'processing'
            order.save()

            return Response({
                "status": "success",
                "payment_url": response['GatewayPageURL']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "failed",
                "message": "Payment initiation failed."
            }, status=status.HTTP_400_BAD_REQUEST)

    except Order.DoesNotExist:
        return Response({
            "status": "failed",
            "message": "Order not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": "failed",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)







@api_view(['POST'])
def payment_success(request):
    val_id = request.POST.get('val_id')
    tran_id = request.POST.get('tran_id')

    validation_url = f"https://securepay.sslcommerz.com/validator/api/validationserverAPI.php?val_id={val_id}&store_id={store_id}&store_passwd={store_pass}&format=json"

    # Validate payment with SSLCommerz
    try:
        validation_response = requests.get(validation_url)
        validation_data = validation_response.json()

        if validation_data['status'] == 'VALID':
            try:
                # Fetch the order using the transaction ID
                order = Order.objects.get(transaction_id=tran_id)

                # Update the order status
                order.status = 'shipped'  # Payment successful, mark as shipped
                order.save()

                return Response({
                    "status": "success",
                    "message": "Payment was successful and order updated.",
                    "order_id": order.order_id,
                    "grand_total": order.grand_total,
                    "status": order.status
                }, status=status.HTTP_200_OK)

            except Order.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "Order not found."
                }, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({
                "status": "failed",
                "message": "Payment validation failed."
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "status": "failed",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def payment_fail(request):
    tran_id = request.POST.get('tran_id')

    try:
        # Fetch all orders with the matching transaction ID
        orders = Order.objects.filter(transaction_id=tran_id)

        # Check if any orders are found
        if orders.exists():
            canceled_orders = []
            for order in orders:
                order.status = 'canceled'  # Payment failed, mark as canceled
                order.save()

                # Add the canceled order details to the response
                canceled_orders.append({
                    "order_id": order.order_id,
                    "grand_total": order.grand_total,
                    "status": order.status
                })

            return Response({
                "status": "failed",
                "message": "Payment failed, all matching orders canceled.",
                "orders": canceled_orders
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "failed",
                "message": "Order not found."
            }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": "failed",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
