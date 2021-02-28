from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ( 'id','username', 'email', 'first_name',)
    readonly_fields = ('id','show_coupons')

    fieldsets = (
    #Primer categoria
        ("Basic info", {
            'fields': (
            ('id',),
            ('email','username'),
            ('first_name', 'last_name'),
            ('password',),
            ('groups',),
            ('user_permissions',),
            ('is_staff', 'is_active'),
            ('is_superuser',),
            ('last_login',),
            ('date_joined',),
            ),
        }
        ),
    #Cupones
    ("Cupones",{
        'fields':(
            ('show_coupons',),
        ),
    }),
    )

    def show_coupons(self, obj):
        return '\n'.join([c.name for c in obj.coupon_set.all()])



class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)
    list_display = ('_id','name', )

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

    list_display = ('name', 'user', 'brand', 'price', 'countInStock', 'out_of_stock', 'rating')
    ordering = ('createdAt', 'rating', 'price', 'countInStock')
    search_fields = ('name', 'user__first__name', 'brand', 'price', 'categories__name')
    list_filter =('categories__name',)

    def post_categories(self, obj):
        return ', '.join([c.name for c in obj.categories.all().order_by('name') ])
    post_categories.short_description = 'Categorias'

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)
    list_display = ('name','user', 'rating')

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt','deliveredAT', 'paidAt')
    list_display = ('_id','user', 'isPaid', 'totalPrice','paymentMethod')
    list_filter =('isPaid',)
    ordering = ('createdAt','deliveredAT', 'paidAt')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('_id', 'order', 'name', 'qty')
    ordering = ('_id',)

class ShippingAdressAdmin(admin.ModelAdmin):
    list_display = ('_id', 'order', 'address', 'city', 'country', 'shippingPrice')
    ordering = ('_id',)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('_id', 'name', 'code', 'discount', 'percentage', 'active')
    ordering = ('_id',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAdress, ShippingAdressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
