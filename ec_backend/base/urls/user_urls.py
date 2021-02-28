from django.urls import path
from base.views import user_views as views


urlpatterns = [
    path('profile/', views.getUserProfile, name ='users-profile'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name ='register'),
    path('', views.getUsers, name ='users'),
    path('<str:pk>/', views.getUserById, name ='user'),
    path('update/<str:pk>/', views.updateUser, name ='user-update'),
    path('delete/<str:pk>/', views.deleteUser, name ='user-delete'),
]
