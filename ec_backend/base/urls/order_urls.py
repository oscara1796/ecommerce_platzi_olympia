from django.urls import path
from base.views import order_views as views


urlpatterns = [
    path('add/', views.addOrderItems, name = 'orders-add'),
    path('myorders/', views.getMyOrders, name = 'my-orders'),
    path('coupons/', views.showAllCoupon, name = 'coupon-all'),
    path('getcoupon/', views.getCoupon, name = 'coupon'),
    path('createcoupon/', views.createCoupon, name = 'coupon-create'),
    path('<str:pk>/', views.getOrderById, name = 'user-order'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name = 'pay-order'),
    path('deletecoupon/<str:pk>/', views.deleteCoupon, name = 'coupon-delete'),
    path('updatecoupon/<str:pk>/', views.updateCoupon, name = 'coupon-update'),
]
