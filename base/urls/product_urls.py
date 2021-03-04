from django.urls import path
from base.views import product_views as views


urlpatterns = [
    path('', views.getProducts, name ='products'),
    path('create/', views.createProduct, name ='product-create'),
    path('uploadimage/', views.uploadImage, name ='product-uploadimage'),
    path('topproducts/', views.getTopProducts, name ='top-products'),
    path('top-products-per-category/', views.getTopProductsPerCategory, name ='getTopProductsPerCategory'),
    path('categories/', views.getCategories, name ='categories'),
    path('createcategories/', views.createCategories, name ='categories-create'),
    path('<str:pk>/', views.getProduct, name ='product'),
    path('update/<str:pk>/', views.updateProduct, name ='product-update'),
    path('delete/<str:pk>/', views.deleteProduct, name ='product-delete'),
    path('createreview/<str:pk>/', views.createProductReview, name ='review-create'),
    path('deletecategories/<str:pk>/', views.deleteCategories, name ='categories-delete'),
    path('updatecategories/<str:pk>/', views.updateCategories, name ='categories-update'),
    path('categories/<str:pk>/', views.getProductsByCategory, name ='product-of-category'),
]
