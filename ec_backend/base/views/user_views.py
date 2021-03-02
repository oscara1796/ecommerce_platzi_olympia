from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from base.serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from base.models import UserStripe, UserPaymentMethodsStripe
from django.contrib.auth.hashers import make_password
from rest_framework import status
import stripe



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithtoken(self.user).data
        print(serializer)

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data= request.data

    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password']),
        )
        print(data)
        customer=stripe.Customer.create(
          name=data['name'],
          email =data['email'],
        )
        user_stripe_id = UserStripe.objects.create(
        user=user,
        stripe_customer_id= customer.id
        )

        serializer = UserSerializerWithtoken(user, many= False)
        return Response(serializer.data)

    except:
        message = {'detail': 'User already exists'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('user deleted')

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = User.objects.get(id=pk)

    data = request.data

    user.first_name = data['name']
    user.last_name = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user_stripe_id = UserStripe.objects.get(user=user)
    customer=stripe.Customer.modify(
    user_stripe_id.stripe_customer_id,
      name=data['name'],
      email =data['email'],
    )

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addCouponToUser(request, pk):
    error_message = 'coupon does not exists'
    try:
            data = request.data
            coupon = data['coupon']
            coupon = Coupon.objects.get(code = coupon.upper())
            user = User.objects.get(id=pk)
            if request.user == user:
                user.coupon_set.add(coupon)

                user.save()
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data)
            else:
                raise Exception('User is not the current request user')
    except Exception as e:
        error_message = e
        message = {'detail': f'{error_message}'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPaymentMethod(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_payment_id=stripe.PaymentMethod.create(
      type="card",
      card={
        "number": data['card-number'],
        "exp_month": data['card-exp-month'],
        "exp_year": data['card-exp-year'],
        "cvc": data['card-cvc'],
      },
    )
    stripe_customer = user.userstripe

    stripe.PaymentMethod.attach(
      stripe_payment_id.id,
      customer=stripe_customer.stripe_customer_id,
    )

    payment_obj = UserPaymentMethodsStripe.objects.all()

    for pay_obj in payment_obj:
        pay_obj.default = False
        pay_obj.save()
    
    paymentuser_method_stripe = UserPaymentMethodsStripe.objects.create(
        user= user,
        stripe_payment_id= stripe_payment_id.id,
        default= True,
    )
    return Response('payment added')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrievePaymentMethods(request, pk):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = User.objects.get(id=pk)
        stripe_customer = user.userstripe
        users_payment_methods= stripe.PaymentMethod.list(
          customer=stripe_customer.stripe_customer_id,
          type="card",
        )
        print(users_payment_methods)
        return Response(users_payment_methods)
    except:
        message = {'detail': 'User does not have payment methods'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)
