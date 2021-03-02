from django.urls import path
from payments import views as payment_views


urlpatterns = [
    path('test-payment/', payment_views.test_payment),
]
