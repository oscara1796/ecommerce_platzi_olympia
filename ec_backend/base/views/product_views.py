from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, Category, Review
from base.serializer import ProductSerializer, CategorySerializer
from decimal import Decimal
from rest_framework import status
import stripe


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    print('QUERY: ', query)
    if query != None:
        products = Product.objects.filter(name__icontains= query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getTopProducts(request):

    products = Product.objects.filter(rating__gte=4).order_by('rating')[0:5]
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
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user
    product = Product.objects.create(
        user = user,
        name = 'Sample name',
        price = 0,
        brand = 'sample brand',
        countInStock = 0,
        description= ''
    )
    stripe_product= stripe.Product.create(name=product.name, metadata={'_id': product._id })

    product.stripe_product_id = stripe_product.id
    product.save()

    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
def updateProduct(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = Decimal(data['countInStock'])
    product.description = data['description']

    stripe_product= stripe.Product.modify(
      product.stripe_product_id,
      name= data['name'],
      description= data['description'],
      attributes= [data['brand']],
    )
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

@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data = request.data

    product = Product.objects.get(_id = data['product_id'])

    product.image = request.FILES.get('image')
    # stripe_product= stripe.Product.modify(
    #   product.stripe_product_id,
    #   images=[product.image.url],
    # )

    product.save()

    return Response("image was uploaded")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data  = request.data

    #1 already exists a review
    already_exists = product.review_set.filter(user=user).exists()

    if already_exists:
        content = {'details': 'Product already reviewed'}
        return Response(content, status = status.HTTP_400_BAD_REQUEST)
    #2 no rating  or 0
    elif int(data['rating']) <= 0:
        content = {'details': 'Please select a rating'}
        return Response(content, status = status.HTTP_400_BAD_REQUEST)
    #3  Create a Review
    else:
        review = Review.objects.create(
            user = user,
            product = product,
            name= user.first_name,
            rating= data['rating'],
            comment= data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total=0

        for i in reviews:
            total += i.rating

        product.rating = total // product.numReviews

        product.save()

        return Response({'detail':'Review Added'})
