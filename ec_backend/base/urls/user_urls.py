from django.urls import path
from base.views import user_views as views


urlpatterns = [
    path('profile/', views.getUserProfile, name ='users-profile'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name ='register'),
    path('', views.getUsers, name ='users'),
    path('<str:pk>/', views.getUserById, name ='user'),
    path('addcoupon/<str:pk>/', views.addCouponToUser, name ='user-addcoupon'),
    path('update/<str:pk>/', views.updateUser, name ='user-update'),
    path('delete/<str:pk>/', views.deleteUser, name ='user-delete'),
    path('addpaymentmethod/<str:pk>/', views.addPaymentMethod, name ='user-addPaymentMethod'),
    path('retrievepaymentmethod/<str:pk>/', views.retrievePaymentMethods, name ='user-addPaymentMethod'),
    path('changedefaultpayment/<str:pk>/', views.changeDefaultPaymentMethod, name ='user-changeDefaultPaymentMethod'),
    path('addshippingaddress/<str:pk>/', views.addShippingaddress, name ='user-addShippingaddress'),
    path('retrieveshippingaddress/<str:pk>/', views.retrieveShippingaddress, name ='user-retrieveShippingaddress'),
    path('deleteshippingaddress/<str:pk>/', views.deleteShippingaddress, name ='user-deleteShippingaddress'),
    path('changedefault/shippingaddress/<str:pk>/', views.changeDefaultShippingaddress, name ='user-changeDefaultShippingaddress'),
]
