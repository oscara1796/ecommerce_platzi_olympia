from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, OrderItem, Order, ShippingAdress, Coupon, UserPaymentMethodsStripe
from base.serializer import ProductSerializer, OrderSerializer, CouponSerializer

from rest_framework import status
from decimal import Decimal
from datetime import datetime
from currency_converter import CurrencyConverter


def stripe_payment_management(data, user, convertion, currency):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payment_intent= None
    if user.is_authenticated:
        stripe_customer = user.userstripe
        payment_methods =UserPaymentMethodsStripe.objects.filter(user=user)
        default_payment_method= None
        if len(payment_methods) != 0:
            for payment_method in payment_methods:
                if payment_method.default == True:
                    default_payment_method= payment_method
                    break


        else:
            stripe_payment_id=stripe.PaymentMethod.create(
              type="card",
              card={
                "number": data['card-number'],
                "exp_month": data['card-exp-month'],
                "exp_year": data['card-exp-year'],
                "cvc": data['card-cvc'],
              },
            )

            stripe.PaymentMethod.attach(
              stripe_payment_id.id,
              customer=stripe_customer.stripe_customer_id,
            )

            payment_obj = UserPaymentMethodsStripe.objects.filter(user=user)

            for pay_obj in payment_obj:
                pay_obj.default = False
                pay_obj.save()

            default_payment_method = UserPaymentMethodsStripe.objects.create(
                user= user,
                stripe_payment_id= stripe_payment_id.id,
                default= True,
            )

        payment_intent=stripe.PaymentIntent.create(
        customer=stripe_customer.stripe_customer_id,
        payment_method=default_payment_method.stripe_payment_id,
        currency=currency.lower(), # you can provide any currency you want
        amount=float(convertion))
    else:
        stripe_payment_id=stripe.PaymentMethod.create(
          type="card",
          card={
            "number": data['card-number'],
            "exp_month": data['card-exp-month'],
            "exp_year": data['card-exp-year'],
            "cvc": data['card-cvc'],
          },
        )
        payment_intent=stripe.PaymentIntent.create(
        payment_method=stripe_payment_id.id,
        currency=currency.lower(), # you can provide any currency you want
        amount=float(convertion))

    return payment_intent




@api_view(['POST'])
def addOrderItems(request):
    location = request.geolocation
    currency =str(location['raw_data']['currency_code']).lower()
    c = CurrencyConverter()
    convertion = c.convert(float(data['totalPrice']), 'MXN', currency.upper())
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = None
    data = request.data

    #Verify payment methods in stripe
    print("USER IS AUTHENTICATED: ", request.user.is_authenticated)
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.user.is_authenticated:
            user = request.user
        if str(data['paymentMethod']).lower() == 'stripe':
            payment_intent=stripe_payment_management(data, user, convertion, currency)

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
