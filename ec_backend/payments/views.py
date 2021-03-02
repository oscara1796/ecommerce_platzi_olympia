from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import stripe
import pycountry
# from django_ip_geolocation.decorators import with_ip_geolocation


# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# @with_ip_geolocation
@api_view(['POST'])
def test_payment(request):
    # ip = get_client_ip(request)
    location = request.geolocation
    print(location)
    print('CURRENCY: ', location['raw_data']['currency_code'])

    stripe.api_key = settings.STRIPE_SECRET_KEY
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, currency='pln',
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)
