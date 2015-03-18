__author__ = 'alejandroarciniegafernandez'
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


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
    existencias=models.IntegerField()

    def __unicode__(self):
        return self.nombre


class Articulo(Product):
    familia=models.ForeignKey(Familia)
    tallas=models.ManyToManyField(Talla)
    marca= models.CharField(max_length=255)
    devolucion= models.CharField(max_length=255)
    esoferta=models.BooleanField(blank=True)
    imagen= models.ImageField(upload_to='media')
    proveedor= models.ForeignKey(Proveedor)

    class Meta:
        ordering = ['marca']




class Oferta(models.Model):
    descuento=models.IntegerField()
    fechainicio=models.DateField()
    fechafin=models.DateField()
    precioviejo=models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    articulo=models.OneToOneField(Product)



class FormaPago(models.Model):
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre


class Compania(models.Model):
    nombre= models.CharField(max_length=255)
    contacto= models.CharField(max_length=255)
    preciopeso1=models.DecimalField(max_digits=5, decimal_places=2)
    preciopeso2=models.DecimalField(max_digits=5, decimal_places=2)
    preciopeso3=models.DecimalField(max_digits=5, decimal_places=2)
    gastoextra= models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.nombre


class Compra(models.Model):
    fechacompra= models.DateField()
    cantidad= models.IntegerField()
    formaenvio= models.CharField(max_length=255)
    precio= models.DecimalField(max_digits=5, decimal_places=2)
    deporuser = models.OneToOneField(DeporUser)
    articulo= models.ManyToManyField(Articulo)
    formapago=models.OneToOneField(FormaPago)
    compania=models.OneToOneField(Compania)

    def __unicode__(self):
        return self.identificador


class ComentaArticulo(models.Model):
    valoracion= models.IntegerField()
    opinion= models.CharField(max_length=255)
    articulo= models.ForeignKey(Articulo)
    user = models.ForeignKey(User)
    fecha=models.DateField()
    recomendar=models.BooleanField(default=False)

    def __unicode__(self):
        return self.opinion


class ComentaCompra(models.Model):
    opinion= models.CharField(max_length=255)
    compra= models.OneToOneField(Compra)
    user = models.OneToOneField(User)
    fecha= models.DateField()

    def __unicode__(self):
        return self.opinion


class Factura(models.Model):
    nfactura= models.IntegerField()
    nif= models.CharField(max_length=255)
    precio=models.DecimalField(max_digits=5, decimal_places=2)
    direccion= models.CharField(max_length=255)
    compra = models.ForeignKey(Compra)
    precioenvio= models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.nfactura


class Gusto(models.Model):
    fecha= models.DateField()
    deporuser = models.ForeignKey(DeporUser)
    marca= models.ManyToManyField(Marca)


