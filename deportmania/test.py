__author__ = 'alejandro'
# -*- coding: utf-8 -*-
from decimal import Decimal
from shop.models.productmodel import Product
from shop.models.ordermodel import Order, OrderItem
from shop.models.cartmodel import Cart,CartItem
from django.test.testcases import TestCase
from deportmania.models import *
from datetime import date
from django.test import Client
from mock import Mock
from django.core.urlresolvers import reverse
from shop.addressmodel.models import Address,Country


class ProductTestCase(TestCase):

    def setUp(self):
        self.product = Product()
        self.product.name = 'test'
        self.product.unit_price = Decimal('1.0')
        self.product.slug = 'test'
        self.familia= Familia()
        self.familia.nombre='testfamilia'
        self.familia.pesomedio=500
        self.familia.save()
        self.c=Client()
        self.request=Mock()
        self.user=User()
        self.user.username='ispp1'
        self.user.is_superuser=1
        self.user.email="alemaki92@gmail.com"
        self.user.password='ispp'
        self.user.save()
        self.deporuser=DeporUser()
        self.deporuser.djangoUser=self.user
        self.deporuser.birthday=date.today()
        self.deporuser.gender='m'
        self.deporuser.email='prueba2@gmail.com'
        self.deporuser.poblacion='utrera'
        self.deporuser.save()
        self.cart=Cart()
        self.cart.user=self.user
        self.cart.date_created='2015-05-05'
        self.cart.last_updated='2015-05-05'
        self.cart.save()
        self.c.post('/login',{'usernamelogin':'ispp','passwordlogin':'ispp'})

    def assertCartHasItems(self, expected):
        cart_response=self.c.get(reverse('cart'))
        cart = cart_response.context["cart"]
        count = sum([cart_item.quantity for cart_item in cart.items.all()])
        self.assertEqual(count, expected)

    def add_product_to_cart(self, product):
        post = {'add_item_id':2,'add_item_quantity':1,'talla':'S'}
        return self.client.post(reverse('cart_item_add'), post)

    def test_crear_producto(self):
        producto=Product.objects.create(name='hola',unit_price=3,active=1)
        self.assertTrue(isinstance(producto,Product))


    def test_crear_articulo(self):
        proveedor=Proveedor.objects.create(nombre='prov',direccion='nada',contacto='nada')
        articulo=Articulo.objects.create(product_ptr_id=self.product.id,familia=self.familia,proveedor=proveedor,marca='marca',
                                         esoferta=False,devolucion=3,imagen='nada.jpg')
        self.assertTrue(isinstance(articulo,Articulo))
        self.assertTrue(isinstance(proveedor,Proveedor))

    def test_crear_familia(self):
        prueba=Familia.objects.all()
        response=self.c.post('/crearfamilia',{'nombre':'familia1','pesomedio':100,'submit':'submit'})
        self.assertEqual(response.status_code,200)
        familia=Familia.objects.all()

    def test_modificar_familia(self):
        print("Familia id",self.familia.id)
        response=self.c.post('/familia/'+str(self.familia.id)+'/',{'nombre':'prueba','pesomedio':400,'modify':'modify'})
        self.assertEqual(response.status_code,200)

    def test_eliminar_familia(self):
        self.c.post('/login',{'usernamelogin':'ispp','passwordlogin':'ispp'})
        response=self.c.post('/familia/'+str(self.familia.id)+'/',{'delete':'delete'})
        familia1=Familia.objects.all()
        print("Despues borrar",len(familia1))
        self.assertEqual(response.status_code,200)

    def test_registro(self):
        response=self.c.post('/register',{'username':'prueba1','email':'ale@gmail.com','password':'password',
                                 'birthday':'1992-09-21','poblacion':'utrera','gender':'m','submit':'submit'})
        self.assertEqual(response.status_code,302)

    def test_generar_factura(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.post('/generafactura',{'nombre':'nombre','apellidos':'apellidos','dni':'dni','empresa':'empresa',
                               'nif':'nif','pedido':136,'submit':'submit'})
        self.assertEqual(response.status_code,200)

    def test_registrar_articulo(self):
        response=self.c.post('/creararticulo',{'nombre':'nombre','precio':5,'marca':'marca','proveedor':'Adidas','devolucion':4,
                                               'imagen':'prueba.jpg','famili':'Calzado Padel','submit':'submit'})
        self.assertEqual(response.status_code,200)


    def test_modificar_articulo(self):
        response=self.c.post('/modarticulo/4/',{'nombre':'articulo','precio':52,'marca':'marca1','proveedor':'Adidas','devolucion':4,
                                               'imagen':'prueba.jpg','familia':'Calzado Nike','modify':'modify'})
        self.assertEqual(response.status_code,200)

    def test_eliminar_articulo(self):
        response=self.c.post('/modarticulo/4/',{'delete':'delete'})
        self.assertEqual(response.status_code,200)

    def test_insertar_comentario(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.post('/articulo/2/',{'opinion':'prueba de comentario','valoracion':4,'recomendar':'si','submit':'submit','user':'alearcfer'})
        self.assertEqual(response.status_code,200)

#Probar en casa este
    def test_correo(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.post('/contacto',{'nombre':'alejandro','email':'alearcfer1992@gmail.com',
                                          'comentario':'prueba correo','submit':'submit'} )

    def test_incluir_carro(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.post(reverse('cart_item_add'),{'add_item_id':2,'add_item_quantity':1,'talla':'S'})
        self.assertEqual(response.status_code,302)
        self.assertCartHasItems(1)

    def test_actualizar_carro(self):
        self.c.post(reverse('cart_item_add'),{'add_item_id':2,'add_item_quantity':1,'talla':'S'})
        cart_response=self.c.get(reverse('cart'))
        cart = cart_response.context["cart"]
        cart_item_id = cart.items.all()[0].id
        print("ID",int(cart_item_id))
        response = self.client.post(reverse("cart_update"), {
            'form-0-id': int(cart_item_id),
            'form-0-quantity': 2,})
        self.assertEqual(response.status_code, 302)
        self.assertCartHasItems(2)

    def test_vaciar_carro(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.post(reverse('cart_delete'),{'submit':'submit'})
        self.assertEqual(response.status_code,302)
        self.assertCartHasItems(0)

    def test_busqueda(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.get('/busqueda/',{'texto':'nike','submit':'submit'})
        self.assertEqual(response.status_code,200)

    def test_get_cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_listar_pedido(self):
        self.c.post('/login',{'usernamelogin':'alearcfer','passwordlogin':'ispp'})
        response=self.c.get('/pedidos')
        self.assertEqual(response.status_code,200)

    def test_crear_pedido(self):
        self.order = Order()
        self.order.order_subtotal = Decimal('10')
        self.order.order_total = Decimal('10')
        self.order.shipping_cost = Decimal('0')

        self.order.shipping_address_text = 'shipping address example'
        self.order.billing_address_text = 'billing address example'

        self.order.save()

        self.assertTrue(isinstance(self.order,Order))

    def test_crear_pedido_desde_carro(self):
        self.cart.add_product(self.product,talla="S",quantity=1)
        self.cart.update(self.request)
        self.cart.save()

        o = Order.objects.create_from_cart(self.cart, self.request)

        self.assertNotEqual(o, None)

        ois = OrderItem.objects.filter(order=o)
        cis = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(len(ois), len(cis))

        self.assertEqual(o.order_subtotal, self.cart.subtotal_price)
        self.assertEqual(o.order_total, self.cart.total_price)

    def test_crear_oferta(self):
        response=self.c.post('/crearoferta',{'descuento':10,'fechainicio':'2015-05-05','fechafin':'2015-06-06',
                                             'articulo':'','submit':'submit'})