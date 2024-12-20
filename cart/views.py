from .modules import *


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            color = request.data.get('color')
            size = request.data.get('size')

            if not product_id:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Product ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the product is on sale and use the sale price if available
            price_to_use = product.salePrice if product.on_sale else product.regularPrice

            # Check if the product is already in the cart, update if it is
            cart_item_qs = Cart.objects.filter(customer=customer, product=product, color=color, size=size)

            if cart_item_qs.exists():
                cart_item = cart_item_qs.first()
                cart_item.quantity += quantity
                cart_item.save()
                message = 'Cart item updated successfully'
            else:
                # Create a new cart item
                cart_item = Cart.objects.create(
                    customer=customer,
                    product=product,
                    color=color,
                    size=size,
                    quantity=quantity
                )
                message = 'Cart item added successfully'

            # Serialize the cart item
            serializer = CartSerializer(cart_item)
            return Response({
                'code': status.HTTP_200_OK,
                'message': message,
                'cart_item': serializer.data
            }, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, customer_id, cart_id):

        try:

            customer = Customer.objects.get(id=customer_id)

            cart_item = Cart.objects.get(id=cart_id, customer=customer)

            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            color = request.data.get('color')
            size = request.data.get('size')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Product not found'
                }, status=status.HTTP_404_NOT_FOUND)

            cart_item.product = product
            cart_item.quantity = quantity
            cart_item.color = color
            cart_item.size = size
            cart_item.save()

            serializer = CartSerializer(cart_item)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Cart updated successfully',
                'cart_item': serializer.data
            }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id, cart_id):

        try:
            customer = Customer.objects.get(id=customer_id)

            cart_item_qs = Cart.objects.filter(customer=customer, id=cart_id)

            if cart_item_qs.exists():
                cart_item = cart_item_qs.first()
                cart_item.delete()
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Cart item deleted successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Cart item with id {cart_id} not found for customer {customer_id}'
                }, status=status.HTTP_404_NOT_FOUND)

        except Customer.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_carts_by_id(request, customer_id):
    try:
        customers = Customer.objects.get(id=customer_id)
        carts = Cart.objects.filter(customer=customers)
        serializer = CartSerializer(carts, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message': "Get all carts successfully",
            'data': serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_coupon(request):
    coupon_code = request.data.get('coupon_code')

    if not coupon_code:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Coupon code is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = request.user  # Get the user from the token
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Customer not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        discount = Discount.objects.get(code=coupon_code)

        cart_items = Cart.objects.filter(customer=customer)

        total_discounted_price = 0
        for cart_item in cart_items:
            product_price = cart_item.product.salePrice if cart_item.product.on_sale else cart_item.product.regularPrice

            discounted_price = product_price - discount.coupon_amount
            total_discounted_price += discounted_price * cart_item.quantity

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Coupon applied successfully.',
            'total_discounted_price': total_discounted_price
        }, status=status.HTTP_200_OK)

    except Discount.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Discount code not found.'
        }, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_cart_on_order(request):
    user = request.user

    try:
        # Check if an order was created successfully
        if Order.objects.filter(user=user).exists():
            # Clear all items in the cart for the user
            Cart.objects.filter(customer=user.customer).delete()

            return Response({
                "message": "Cart cleared successfully after order creation."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "No recent orders found for the user."
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
