from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserStripe(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id= models.CharField(max_length=100, verbose_name= "stripe customer id")
    createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")

    class Meta:
        verbose_name= "User-stripe-id"
        verbose_name_plural= "User-stripe-ids"
        ordering = ['_id']

    def __str__(self):
        return self.stripe_customer_id

class UserPaymentMethodsStripe(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    stripe_payment_id= models.CharField(max_length=100, verbose_name= "stripe ")
    default = models.BooleanField(default=True, verbose_name="default")
    createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")

    class Meta:
        verbose_name= "User-payment-method-stripe-id"
        verbose_name_plural= "User-payment-method-stripe-ids"
        ordering = ['_id']

    def __str__(self):
        return self.stripe_payment_id


class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name= models.CharField(max_length=100, verbose_name= "Nombre")
    createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")

    class Meta:
        verbose_name= "Categoria"
        verbose_name_plural= "Categorias"
        ordering = ['createdAt']

    def __str__(self):
        return self.name



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Nombre")
    image = models.ImageField(upload_to= 'product_images/', null=True, blank=True, default='/product_images/placeholder.png', verbose_name= "imagen")
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Marca")
    categories = models.ManyToManyField(Category, verbose_name="Categorias")
    description = models.TextField(null=True, blank=True, verbose_name= "Descripción")
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Rating")
    numReviews = models.IntegerField(null=True, blank=True, default=0, verbose_name= "Num. reviews")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Precio")
    countInStock = models.IntegerField(null=True, blank=True, default=0, verbose_name= "Stock")
    out_of_stock = models.BooleanField(default=False, verbose_name="Agotado")
    createdAt= createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")
    stripe_product_id = models.CharField(max_length=200, null=True, blank=True, verbose_name= "stripe_product_id")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Producto"
        verbose_name_plural= "Productos"
        ordering = ['createdAt', 'rating', 'price', 'countInStock']

    def __str__(self):
        return self.name


class Review(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name= models.CharField(max_length=200, null=True, blank=True, verbose_name= "Nombre")
    rating= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Rating")
    comment=  models.TextField(null=True, blank=True, verbose_name= "Descripción")
    createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Review"
        verbose_name_plural= "Reviews"
        ordering = ['createdAt', 'rating']

    def __str__(self):
        return str(self.rating)

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Metodo de pago")
    taxtPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Impuesto")
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Costo de envio")
    discount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Descuento")
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Precio total")
    isPaid = models.BooleanField(default=False, verbose_name="Pagado")
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name= "Fecha de pago")
    isDelivered =  models.BooleanField(default=False, verbose_name="Entregado")
    deliveredAT = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name= "Fecha de entrega")
    createdAt= models.DateTimeField(auto_now_add=True, verbose_name= "Fecha de Creación")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Orden"
        verbose_name_plural= "Ordenes"
        ordering = ['createdAt', '_id']

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Nombre")
    qty = models.IntegerField(null=True, blank=True, default=0, verbose_name= "cantidad")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Precio")
    image = models.ImageField(upload_to= 'orderitems_images/', null=True, blank=True, verbose_name= "imagen")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Orden item"
        verbose_name_plural= "Orden items"
        ordering = ['_id']

    def __str__(self):
        return str(self.name)


class ShippingAdress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Domicilio ")
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Ciudad")
    postalCode = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Codigo Postal")
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name= "País")
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Costo de envio")
    receiver_first_name = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Recibidor primer nombre ")
    receiver_last_name = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Recibidor apellidos")
    default = models.BooleanField(default=True, verbose_name="default")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Domicilio de envio"
        verbose_name_plural= "Domicilios de envio"
        ordering = ['_id']

    def __str__(self):
        return str(self.address)

class Coupon(models.Model):
    user= models.ManyToManyField(User, null=True)
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name= "Nombre de cupon")
    code = models.CharField(max_length=200, null=True, blank=True,unique=True, verbose_name= "Código")
    discount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Descuento")
    percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name= "Porcentaje")
    active = models.BooleanField(default=False, verbose_name="Activo")
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name= "Cupon"
        verbose_name_plural= "Cupones"
        ordering = ['_id']

    def __str__(self):
        return str(self.name)
