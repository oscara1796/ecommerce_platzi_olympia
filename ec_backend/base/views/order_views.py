from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, OrderItem, Order, ShippingAdress, Coupon
from base.serializer import ProductSerializer, OrderSerializer

from rest_framework import status


@api_view(['POST'])
def addOrderItems(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    data = request.data

    orderItems = data['orderItems']
    coupon = data['coupon']
    coupon_exists = Coupon.objects.filter(code=coupon).exists()
    if coupon_exists:
        pass
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxtPrice = data['taxtPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'],
        )
        # (2) Create shipping address
        shipping = ShippingAdress.objects.create(
            order = order,
            address = data['ShippingAdress']['address'],
            city = data['ShippingAdress']['city'],
            country  = data['ShippingAdress']['country'],
            city = data['ShippingAdress']['city'],
        )
        # (3) Create order items and set the order to  order Item  relationship
        for i in orderItems:
            product = Product.objects.get(_id =i['product'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image= product.image.url,
            )

            # (4) update Stock
            product.countInStock -= item.qty
            product.save()
    serializer = OrderSerializer(order, many = True)
    return Response('Order')
