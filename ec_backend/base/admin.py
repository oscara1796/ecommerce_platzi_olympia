from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

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
