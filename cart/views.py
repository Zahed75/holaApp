from.modules import *




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        user = request.user
        product_ids = request.data.get('product_id', [])
        quantity = request.data.get('quantity', 1)  # Default quantity to 1 if not provided

        if not product_ids:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Product ID(s) are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_data = []
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the product is already in the cart
            cart_item, created = Cart.objects.get_or_create(
                customer=user.customer,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # If the cart item already exists, update the quantity
                cart_item.quantity += quantity
                cart_item.save()

            # Add product information and cart id to the response
            cart_data.append({
                'cart_id': cart_item.id,  # Include the cart item's id
                'id': product.id,
                'name': product.productName,
                'description': product.productDescription,
                'price': product.salePrice if product.on_sale else product.regularPrice,
                'quantity': cart_item.quantity,
                'added_at': cart_item.added_at
            })

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Products added to cart successfully',
            'cart_items': cart_data  # Include detailed product information and cart_id
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_cart(request, cart_id):
    try:
        user = request.user
        product_ids = request.data.get('product_id', [])
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        if not product_ids:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Product ID(s) are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_cart_data = []

        # Handle multiple products
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                cart_item = Cart.objects.get(customer=user.customer, product=product)
            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except Cart.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} is not in the cart'
                }, status=status.HTTP_404_NOT_FOUND)

            # Update the quantity
            cart_item.quantity = quantity
            cart_item.save()

            # Add updated product information to the response
            updated_cart_data.append({
                'cart_id': cart_item.id,
                'id': product.id,
                'name': product.productName,
                'description': product.productDescription,
                'price': product.salePrice if product.on_sale else product.regularPrice,
                'quantity': cart_item.quantity,
                'added_at': cart_item.added_at
            })

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Cart updated successfully',
            'updated_cart_items': updated_cart_data  # Return updated cart item details
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, cart_id):
    try:
        user = request.user
        product_ids = request.data.get('product_id', [])

        if not product_ids:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Product ID(s) are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle multiple products
        for product_id in product_ids:
            try:
                # Check if the product exists
                product = Product.objects.get(id=product_id)

                # Ensure the cart item belongs to the current user and the correct cart
                cart_item = Cart.objects.get(id=cart_id, customer=user.customer, product=product)

            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except Cart.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': f'Product with id {product_id} is not in the cart'
                }, status=status.HTTP_404_NOT_FOUND)

            # Delete the cart item
            cart_item.delete()

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Products removed from cart successfully',
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_carts_by_customer(request, customer_id):
    try:
        # Fetch the customer based on the provided customer_id
        customer = Customer.objects.get(id=customer_id)

        # Fetch all cart items for this customer
        cart_items = Cart.objects.filter(customer=customer)

        if not cart_items.exists():
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'No cart items found for this customer'
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize the cart items and their associated products
        cart_data = []
        for item in cart_items:
            product = item.product
            cart_data.append({
                'cart_id': item.id,
                'product_id': product.id,
                'name': product.productName,
                'description': product.productDescription,
                'price': product.salePrice if product.on_sale else product.regularPrice,
                'quantity': item.quantity,
                'added_at': item.added_at
            })

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Cart items fetched successfully',
            'cart_items': cart_data
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

