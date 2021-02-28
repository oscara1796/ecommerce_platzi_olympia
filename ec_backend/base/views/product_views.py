from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, Category
from base.serializer import ProductSerializer, CategorySerializer
from decimal import Decimal
from rest_framework import status


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('product deleted')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(
        user = user,
        name = 'Sample name',
        price = 0,
        brand = 'sample brand',
        countInStock = 0,
        description= ''
    )
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = Decimal(data['countInStock'])
    product.description = data['description']
    # product.categories = data['categories']
    try:
        product.categories.clear()
        cat_list = data['categories'].split(",")
        for category in cat_list:
            cat = Category.objects.get(_id=category)
            product.categories.add(cat)
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail':'Category does not exists'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()

    serializer = CategorySerializer(categories, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCategories(request):
    data = request.data
    categories = Category.objects.create(
    name = data['name']
    )

    serializer = CategorySerializer(categories, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategories(request, pk):
    category = Category.objects.get(_id=pk)
    category.delete()

    return Response('category deleted')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCategories(request, pk):
    category = Category.objects.get(_id=pk)
    data = request.data
    category.name = data['name']
    category.save()
    serializer = CategorySerializer(category, many=False)

    return Response(serializer.data)

@api_view(['GET'])
def getProductsByCategory(request, pk):
    category = Category.objects.get(_id=pk)

    products_of_category = category.product_set.all()

    serializer = ProductSerializer(products_of_category, many=True)

    return Response(serializer.data)
