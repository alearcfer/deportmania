__author__ = 'alejandroarciniegafernandez'
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from shop.models import Order
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre


class DeporUser(models.Model):
    djangoUser = models.OneToOneField(User)
    birthday = models.DateField()
    SEX = (("m", "Male"), ("f", "Female"),)
    gender = models.CharField(max_length=1, choices=SEX)
    email = models.EmailField()
    poblacion = models.CharField(max_length=255)


class Familia(models.Model):
    nombre = models.CharField(max_length=255)
    pesomedio = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre


class Deporte(models.Model):
    nombre=models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre


class numerocuenta(models.Model):
    numero=models.IntegerField()


class Talla(models.Model):
    nombre=models.CharField(max_length=5)

    def __unicode__(self):
        return self.nombre



class Articulo(Product):
    familia=models.ForeignKey(Familia)
    tallas=models.ManyToManyField(Talla, blank=True, through="TallaArticulo")
    marca= models.CharField(max_length=255)
    devolucion= models.CharField(max_length=255,blank=True)
    esoferta=models.BooleanField(blank=True)
    imagen= models.ImageField(upload_to='media', blank=True)
    proveedor= models.ForeignKey(Proveedor,blank=True)

    class Meta:
        ordering = ['marca']
    def __unicode__(self):
        return self.name

class Articulo_rating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(DeporUser, related_name="rating_articulo_luser")
    articulo= models.ForeignKey(Articulo)

    def __unicode__(self):
        return str(self.rating)

class TallaArticulo(models.Model):
    articulo=models.ForeignKey(Articulo)
    talla=models.ForeignKey(Talla)
    existencias=models.IntegerField()


class Oferta(models.Model):
    descuento=models.IntegerField()
    fechainicio=models.DateField()
    fechafin=models.DateField()
    precioviejo=models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    articulo=models.OneToOneField(Product)


class Compania(models.Model):
    nombre= models.CharField(max_length=255)
    contacto= models.CharField(max_length=255)
    preciopeso1=models.DecimalField(max_digits=5, decimal_places=2)
    preciopeso2=models.DecimalField(max_digits=5, decimal_places=2)
    preciopeso3=models.DecimalField(max_digits=5, decimal_places=2)
    gastoextra= models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.nombre


class ComentaArticulo(models.Model):
    valoracion= models.IntegerField()
    opinion= models.CharField(max_length=255)
    articulo= models.ForeignKey(Articulo)
    user = models.ForeignKey(User)
    fecha=models.DateField()
    recomendar=models.BooleanField(default=False)

    def __unicode__(self):
        return self.opinion


class Factura(models.Model):
    nfactura= models.IntegerField()
    nif= models.CharField(max_length=255)
    precio=models.DecimalField(max_digits=5, decimal_places=2)
    direccion= models.CharField(max_length=255)
    compra = models.ForeignKey(Order)
    precioenvio= models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.nfactura


class Gusto(models.Model):
    fecha= models.DateField()
    deporuser = models.ForeignKey(DeporUser)
    marca= models.ManyToManyField(Marca)


