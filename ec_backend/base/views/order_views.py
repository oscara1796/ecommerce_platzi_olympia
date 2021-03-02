from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, OrderItem, Order, ShippingAdress, Coupon
from base.serializer import ProductSerializer, OrderSerializer, CouponSerializer

from rest_framework import status
from decimal import Decimal
from datetime import datetime


@api_view(['POST'])
def addOrderItems(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = None
    data = request.data

    #Verify payment methods in stripe
    print("USER IS AUTHENTICATED: ", request.user.is_authenticated)
    if request.user.is_authenticated:
        user = request.user
        stripe_customer = user.userstripe
        custom_payment_methods= stripe.PaymentMethod.list(
          customer=stripe_customer.stripe_customer_id,
          type="card",
        )

        if len(custom_payment_methods.data) == 0:
            stripe_payment=stripe.PaymentMethod.create(
              type="card",
              card={
                "number": data['card-number'],
                "exp_month": data['card-exp-month'],
                "exp_year": data['card-exp-year'],
                "cvc": data['card-cvc'],
              },
            )
            stripe.PaymentMethod.attach(
              stripe_payment.id,
              customer=stripe_customer.stripe_customer_id,
            )
        else:
            pass

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxtPrice = Decimal(data['taxtPrice']),
            shippingPrice = Decimal(data['shippingPrice']),
            totalPrice = Decimal(data['totalPrice']),
        )
        coupon = str(data['coupon'])
        coupon_exists = Coupon.objects.filter(code=coupon.upper()).exists()
        if coupon_exists:
            coupon = Coupon.objects.get(code=coupon.upper())
            if coupon.discount:
                order.discount =  Decimal(coupon.discount)
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
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer  = OrderSerializer(orders, many= True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    user = request.user
    orders = Order.objects.all()
    serializer  = OrderSerializer(orders, many= True)

    return Response(serializer.data)

@api_view(['GET'])
def getOrderById(request, pk):
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

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAT =datetime.now()
    order.save()

    return Response('Order was delivered')

@api_view(['GET'])
@permission_classes([IsAdminUser])
def showAllCoupon(request):
    coupons = Coupon.objects.all()
    serializer = CouponSerializer(coupons, many= True)
    return Response(serializer.data)


@api_view(['POST'])
def getCoupon(request):
    data= request.data
    coupon = str(data['coupon'])
    print(coupon)
    try:
        coupon = Coupon.objects.get(code = coupon.upper())
        serializer = CouponSerializer(coupon, many= False)
        return Response(serializer.data)
    except:
        return Response({'detail':'coupon does not exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCoupon(request, pk):
    data= request.data
    coupon = Coupon.objects.get(_id = pk)
    coupon.delete()
    return Response({'Coupon deleted'})


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def createCoupon(request):
    try:
        data= request.data

        coupon = Coupon.objects.create(
            name = data['name'],
            code = data['code'],
            active = data['active'].lower().title()
        )

        if data['discount']:
            coupon.discount = Decimal(data['discount'])
        elif data['percentage']:
            coupon.percentage = Decimal(data['percentage'])

        coupon.save()
        serializer = CouponSerializer(coupon, many= False)
        return Response(serializer.data)
    except:
        return Response({'detail':'Can\'t create coupon verify code must be unique'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCoupon(request, pk):
    try:
        data= request.data

        coupon = Coupon.objects.get(_id=pk)
        coupon.name = data['name'],
        coupon.code = data['code'],
        coupon.active = data['active'].lower().title()

        if data['discount']:
            coupon.discount = Decimal(data['discount'])
        elif data['percentage']:
            coupon.percentage = Decimal(data['percentage'])

        coupon.save()
        serializer = CouponSerializer(coupon, many= False)
        return Response(serializer.data)
    except:
        return Response({'detail':'Can\'t modify coupon verify code must be unique'}, status=status.HTTP_400_BAD_REQUEST)
