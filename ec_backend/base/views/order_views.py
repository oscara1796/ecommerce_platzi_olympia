from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, OrderItem, Order, ShippingAdress, Coupon
from base.serializer import ProductSerializer, OrderSerializer

from rest_framework import status
from decimal import Decimal
from datetime import datetime


@api_view(['POST'])
def addOrderItems(request):
    user = None
    print("USER IS AUTHENTICATED: ", request.user.is_authenticated)
    if request.user.is_authenticated:
        user = request.user

    data = request.data

    orderItems = data['orderItems']

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
        coupon = str(data['coupon'])
        coupon_exists = Coupon.objects.filter(code=coupon.upper()).exists()
        if coupon_exists:
            coupon = Coupon.objects.get(code=coupon.upper())
            if coupon.discount:
                order.discount =  float(coupon.discount)
            else:
                order.discount =  Decimal(order.totalPrice)*Decimal(coupon.percentage)
            order.save()
        # (2) Create shipping address
        shipping = ShippingAdress.objects.create(
            order = order,
            address = data['ShippingAdress']['address'],
            postalCode = data['ShippingAdress']['postalCode'],
            country  = data['ShippingAdress']['country'],
            city = data['ShippingAdress']['city'],
        )

        if not request.user.is_authenticated:
            shipping.receiver_first_name = data['ShippingAdress']['receiver_first_name']
            shipping.receiver_last_name = data['ShippingAdress']['receiver_last_name']
            shipping.save()
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

        serializer = OrderSerializer(order, many = False)
        return Response(serializer.data)

@api_view(['GET'])
def getOrderById(request, pk):

    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        serializer = OrderSerializer(order, many= False)

        return Response(serializer.data)
    except:
        return Response({'detail':'Order does not exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt =datetime.now()
    order.save()

    return Response('Order was paid')
