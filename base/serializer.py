from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, ShippingAdress, OrderItem, Order, Category, Coupon, Review, UserPaymentMethodsStripe

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only= True)
    _id = serializers.SerializerMethodField(read_only= True)
    isAdmin = serializers.SerializerMethodField(read_only= True)
    coupons = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'coupons']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff



    def get_name(self, obj):
        name= obj.first_name
        if name == '':
            name = obj.email
        return name

    def get_coupons(self, obj):
        coupons_user = obj.coupon_set.all()
        coupons = CouponSerializer(coupons_user, many = True)
        return coupons.data

class UserPaymentMethodsStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethodsStripe
        fields = '__all__'

class UserSerializerWithtoken(UserSerializer):
    token =  serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        reviews = ReviewSerializer(reviews, many=True)
        return reviews.data

class ShippingAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAdress
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAdress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAdress(self, obj):
        try:
            address = ShippingAdressSerializer(obj.shippingadress, many=False)
        except:
            address = False
        return address.data

    def get_user(self, obj):
        try:
            user = UserSerializer(obj.user, many=False)
        except:
            user = False
        return user.data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
