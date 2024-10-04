from.modules import *

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, customer_id):
        """Add a new item to the cart or increment quantity if it exists"""
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

            # Check if the cart item exists with the same product, color, and size
            cart_item_qs = Cart.objects.filter(customer=customer, product=product, color=color, size=size)

            if cart_item_qs.exists():
                # Update the existing cart item by incrementing the quantity
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
            # Fetch customer
            customer = Customer.objects.get(id=customer_id)
            # Fetch cart item based on cart_id
            cart_item = Cart.objects.get(id=cart_id, customer=customer)

            # Update the cart item details
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            color = request.data.get('color')
            size = request.data.get('size')

            # Check if product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Product not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Update cart item fields
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

            # Retrieve the cart item based on customer and cart_id
            cart_item_qs = Cart.objects.filter(customer=customer, id=cart_id)

            if cart_item_qs.exists():
                cart_item = cart_item_qs.first()  # Get the first matching item
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