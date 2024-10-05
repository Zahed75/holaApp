from .modules import *
# Create your views here.




@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def add_product(request):
    try:
        # Handle category IDs
        category_ids = request.data.get('category', '')
        category_ids_list = [int(id.strip()) for id in category_ids.split(',')] if category_ids else []

        # Fetch categories based on the list of IDs
        categories = Category.objects.filter(id__in=category_ids_list)

        # Create the product instance
        product = Product.objects.create(
            productName=request.data.get('productName'),
            productDescription=request.data.get('productDescription'),
            seoTitle=request.data.get('seoTitle'),
            seoDescription=request.data.get('seoDescription'),
            productShortDescription=request.data.get('productShortDescription'),
            color=request.data.get('color'),
            regularPrice=request.data.get('regularPrice'),
            salePrice=request.data.get('salePrice'),
            saleStart=request.data.get('saleStart'),
            saleEnd=request.data.get('saleEnd'),
            fabric=request.data.get('fabric'),
            weight=request.data.get('weight'),
            dimension_length=request.data.get('dimension_length'),
            dimension_width=request.data.get('dimension_width'),
            dimension_height=request.data.get('dimension_height'),
            sizeCharts=request.FILES.get('sizeCharts'),  # Handle sizeCharts image upload
            featureImage=request.FILES.get('featureImage')  # Handle feature image upload
        )

        # Set categories for the product
        product.category.set(categories)

        # Handle gallery image uploads for ProductImage
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image, image_type='gallery')

        # Serialize the product with images
        product_data = ProductSerializer(product).data

        return JsonResponse({
            'message': 'Product added successfully!',
            'product': product_data
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_inventory(request, id):
    try:
        # Fetch the product using the provided ID
        product = Product.objects.get(id=id)
        
        # Update the payload with the product reference
        payload = request.data.copy()
        payload['product'] = product.id

        data_serializer = InventorySerializer(data=payload)
        
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': "Inventory added successfully",
                'data': data_serializer.data,
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "Invalid data",
                'errors': data_serializer.errors,
            })
    
    except Product.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': "Product not found"
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['PUT'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    try:
        productObj = Product.objects.get(id=id)

        # Initialize the serializer with the instance to update
        serializer = ProductSerializer(productObj, data=request.data, partial=True)

        # Ensure the serializer validates correctly
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'payload': serializer.errors,
                'message': 'Something went wrong while validating the data'
            })

        # Handle file uploads separately
        if 'featureImage' in request.FILES:
            productObj.featureImage = request.FILES['featureImage']

        if 'sizeCharts' in request.FILES:
            productObj.sizeCharts = request.FILES['sizeCharts']

        # Handle product gallery images
        if 'images' in request.FILES:
            new_images = request.FILES.getlist('images')
            if new_images:
                # Clear existing gallery images only if new images are provided
                ProductImage.objects.filter(product=productObj, image_type='gallery').delete()

                # Add new images to the product
                for image in new_images:
                    ProductImage.objects.create(product=productObj, image=image, image_type='gallery')

        # Save the updated product after handling all fields
        serializer.save()

        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': "Product updated successfully"
        })

    except Product.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': "Product not found"
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })









@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_inventory(request,id):

    try:
        inventory = Inventory.objects.get(id=id)
        serializers = InventorySerializer(inventory,data=request.data,partial=True)
        if not serializers.is_valid():
            serializers.save()
            return Response({
                 'status': 400,
                'payload': serializers.errors, 
                'message': 'Something Went Wrong'
            })
        serializers.save()
        return Response({
            'status': 200, 
            'payload': serializers.data,
            'message': "Inventroy updated successfully"
        })
    except Exception as e:
         return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_product(request,id):
    try:
        prodcutObj = Product.objects.get(id=id)
        prodcutObj.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product Deleted Successfully!',
            'category_id': id 
        },status=status.HTTP_200_OK)
    
    except Product.DoesNotExist:
         return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Product not found!'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
           return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def inventory_delete(request,id):
    try:
        inventoryObjects = Inventory.objects.get(id=id)
        inventoryObjects.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Inventory Deleted Successfully!',
            'category_id': id 
        },status=status.HTTP_200_OK)
    
    
    except Exception as e:
            return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })




@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()

        data_serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Get All Products Fetched Successfully',
            'data': data_serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['GET'])

def get_products_by_id(request, id):
    try:
        product = Product.objects.get(id=id)
        data_serializer = ProductSerializer(product, many=False, context={'request': request})

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data_serializer.data
        })

    except Product.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Product not found'
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })





@api_view(['GET'])
def get_inventory_by_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.filter(product=product)
        serializer = InventorySerializer(inventory, many=True)

        # Return serialized data
        return Response({
            'code': status.HTTP_200_OK,
            'message': "Inventory details fetched successfully.",
            'data': serializer.data
        })

    except Product.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': "Product not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def filter_products(request):
    # Get query parameters
    search_query = request.query_params.get('products', None)
    category_id = request.query_params.get('category', None)
    size = request.query_params.get('size', None)
    quantity = request.query_params.get('Quantity', None)
    color = request.query_params.get('color', None)
    regular_price = request.query_params.get('regularPrice', None)
    sale_price = request.query_params.get('salePrice', None)
    bar_code = request.query_params.get('barCode', None)
    fabric = request.query_params.get('fabric', None)

    # Start with all products
    queryset = Product.objects.all()

    # Apply search filtering
    if search_query:
        queryset = queryset.filter(
            Q(productName__icontains=search_query) |
            Q(productDescription__icontains=search_query) |
            Q(seoTitle__icontains=search_query)
        )

    # Filter by category
    if category_id:
        queryset = queryset.filter(category__id=category_id)

    # Filter by color
    if color:
        queryset = queryset.filter(color__iexact=color)

    # Filter by regular price
    if regular_price:
        queryset = queryset.filter(regularPrice=regular_price)

    # Filter by sale price
    if sale_price:
        queryset = queryset.filter(salePrice=sale_price)

    # Filter by fabric
    if fabric:
        queryset = queryset.filter(fabric__icontains=fabric)

    # Inventory-related filters
    if size or quantity or bar_code:
        queryset = queryset.filter(
            inventory__size__iexact=size if size else None,
            inventory__quantity=quantity if quantity else None,
            inventory__barCode=bar_code if bar_code else None
        ).distinct()

    # Serialize the filtered queryset
    serializer = ProductSerializer(queryset, many=True)

    return Response(serializer.data)
