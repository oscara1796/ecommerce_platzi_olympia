from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from .models import Product

def updateUser(sender, instance, **kwargs):
    # print("Signal Triggered")
    user = instance
    if user.email != '':
        user.username = user.email

def checkStock(sender, instance, **kwargs):
    # print("Signal Triggered")
    product = instance
    if product.countInStock <= 0:
        product.out_of_stock = True
        product.countInStock = 0
    else:
        product.out_of_stock = False



pre_save.connect(updateUser,sender=User)
pre_save.connect(checkStock,sender=Product)
