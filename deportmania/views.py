__author__ = 'Alejandro'
from deportmania.models import *
from deportmania.forms import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import formats
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.hashers import make_password, pbkdf2
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from shop.models.productmodel import Product
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse


def home(request):
    articulos= Articulo.objects.all().filter(esoferta=False)
    print("HOLA",articulos)
    familias=Familia.objects.all()
    productos=[]
    for elem in articulos:
        prod=get_object_or_404(Product,id=elem.product_ptr_id)
        productos.append(prod)
    duser=request.user
    ofertas=Oferta.objects.all()
    print (request.session.session_key)
    print("User",duser)
    print("productos",productos)
    return render_to_response('home.html',{'articulos':articulos,'productos':productos,'user':duser,'familias':familias,'ofertas':ofertas}, context_instance=RequestContext(request))


def articulo(request,articulo_id):
    print (request.session.session_key)
    objeto=get_object_or_404(Articulo,id=articulo_id)
    producto=get_object_or_404(Product,id=objeto.product_ptr_id)
    familias=Familia.objects.all()
    comenarticulo=ComentaArticulo.objects.all()
    comentacompra=ComentaCompra.objects.all()
    tallas=Talla.objects.all().filter(articulo=objeto)
    compra=Compra.objects.all().filter(articulo=objeto)
    existencias=0
    for elem in tallas:
        existencias=existencias+elem.existencias
    print("Compra",compra)
    print("post",request.POST)
    if request.method == 'POST' and 'submit' in request.POST:
        print("entra")
        user=User.objects.get(username=request.POST['user'])
        opinion=request.POST['opinion']
        valoracion=request.POST['valoracion']
        recomendar=request.POST['recomendar']
        res=False
        if recomendar == 'si':
            res=True
        print(recomendar)
        ComentaArticulo.objects.create(valoracion=valoracion,opinion=opinion,articulo=objeto,user=user,fecha=date.today(),recomendar=res)
    if request.method == 'POST' and 'submitcompra' in request.POST:
        user=User.objects.get(username=request.POST['user'])
        opinion=request.POST['opinion']
        ComentaCompra.objects.create(opinion=opinion,compra=compra,user=user,fecha=date.today())
    return render_to_response('articulo.html',{'articulo':objeto,'familias':familias,
                                               'comenarticulo':comenarticulo,
                                               'comencompra':comentacompra,
                                               'tallas':tallas,'existencias':existencias,
                                              'producto':producto}, context_instance=RequestContext(request))

def ofertas(request):
    ofertas=Oferta.objects.all()
    familias=Familia.objects.all()
    return render_to_response('ofertas.html',{'ofertas':ofertas,'familias':familias}, context_instance=RequestContext(request))

def oferta(request,oferta_id):
    objeto=get_object_or_404(Oferta,id=oferta_id)
    familias=Familia.objects.all()
    articulo=get_object_or_404(Articulo,id=objeto.id)
    producto=get_object_or_404(Product,id=articulo.product_ptr_id)
    comenarticulo=ComentaArticulo.objects.all()
    comentacompra=ComentaCompra.objects.all()
    tallas=Talla.objects.all().filter(articulo=articulo)
    print("post",request.POST)

    if request.method == 'POST' and 'submit' in request.POST:
        print("entra")
        user=User.objects.get(username=request.POST['user'])
        opinion=request.POST['opinion']
        valoracion=request.POST['valoracion']
        recomendar=request.POST['recomendar']
        res=False
        if recomendar == 'si':
            res=True
        print(recomendar)
        ComentaArticulo.objects.create(valoracion=valoracion,opinion=opinion,articulo=objeto,user=user,fecha=date.today(),recomendar=res)
    return render_to_response('oferta.html',{'articulo':articulo,'familias':familias,
                                               'comenarticulo':comenarticulo,'oferta':objeto,
                                               'comencompra':comentacompra,
                                               'tallas':tallas,
                                                'producto':producto}, context_instance=RequestContext(request))
''

def quienes(request):
    return render_to_response('quienes.html', context_instance=RequestContext(request))


def contacto(request):
    if request.method == 'POST' and 'submit' in request.POST:
        msg=""
        mensaje=request.POST['comentario']
        email=request.POST['email']
        subjet="Duda Deportmania"
        to_list=[settings.EMAIL_HOST_USER]
        send_mail(subjet, mensaje, email,to_list, fail_silently=True)
        msg="Mensaje enviado correctamente"
        return render_to_response('home.html',{'msg':msg},context_instance=RequestContext(request))
    return render_to_response('contacto.html',context_instance=RequestContext(request))


def politica(request):
    return render_to_response('politica.html',context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST' and "submit" in request.POST:
        print("entra al formulario")
        userform = DeporUserRegistrationForm(request.POST)
        djangoform = userDjangoForm(request.POST)
        if userform.is_valid() and djangoform.is_valid():
            print("formularios validos")
            #saving to database
            userp = User.objects.create_user(request.POST['username'],request.POST['email'], request.POST['password'])
            profile = userform.save(commit=False)
            profile.djangoUser = userp
            # Now we save the UserProfile model instance.
            profile.save()
            print("registro ok")
            username = request.POST['username']
            hashpassword = request.POST['password']
            UserAccount = authenticate(username=username, password=hashpassword)
            print(UserAccount)
            login(request, UserAccount)
            return HttpResponseRedirect('/home')
        else:
            print(djangoform.errors)
            print(userform.errors)
    return render_to_response('register.html', context_instance=RequestContext(request))


def logeo(request):
    #validation
    loginw = False
    if request.method == 'POST':
        username = request.POST['usernamelogin']
        hashpassword = request.POST['passwordlogin']
        print(username)
        print(hashpassword)
        user = authenticate(username=username, password=hashpassword)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Llevar a la vista principal
                print("Login correcto")
                request.session['carritodecompra'] = []
                return HttpResponseRedirect("/home")

            else:
                # Cuenta no activada
                return HttpResponseRedirect("/error")
        else:
            # Login incorrecto
            print("Login incorrecto")
            loginw = True
            return render_to_response('login.html',
                                      {'loginw': loginw},
                                      context_instance=RequestContext(request))

    return render_to_response('login.html',
                              {'loginw': loginw},
                              context_instance=RequestContext(request))


def terminos(request):
    return render_to_response('terminos.html',context_instance=RequestContext(request))


@login_required(login_url='/home')
def principaladmin(request):
    djangouser=request.user
    print(djangouser)
    return render_to_response('homeadmin.html',{'user':djangouser},context_instance=RequestContext(request))

@login_required(login_url='/home')
def crearproveedor(request):
    print(request.method)
    print(request.POST)
    if request.method == 'POST' and 'submit' in request.POST:
        provform= ProveedorForm(request.POST)
        if provform.is_valid():
            print("Formulario correcto")
            provform.save()
            print("Guardado")
            msg="Proveedor creado correctamente"
            return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
        else:
            print("Error")
    print("No hace nada")
    return render_to_response('crearproveedor.html', context_instance=RequestContext(request))

@login_required(login_url='/home')
def crearcompania(request):
    print(request.method)
    print(request.POST)
    if request.method == 'POST' and 'submit' in request.POST:
        compafor= CompaniaForm(request.POST)
        if compafor.is_valid():
            print("Dentro")
            compafor.save()
            print("creacion compania ok")
            msg="Compania creada correctamente"
            return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
        else:
            print("Error")
    return render_to_response('crearcompania.html',context_instance=RequestContext(request))

@login_required(login_url='home')
def crearoferta(request):
    productos=Product.objects.all()
    print(request.POST)
    if request.method == 'POST' and 'submit' in request.POST:
        articu=Product.objects.get(name=request.POST['articulo'])
        art=get_object_or_404(Articulo,product_ptr_id=articu.id)
        print(articu)
        descuento=request.POST['descuento']
        final=(int(articu.unit_price)*int(descuento))/100
        precionuevo=int(articu.unit_price)-final
        ofer=Oferta.objects.create(descuento=request.POST['descuento'], fechainicio=request.POST['fechainicio'],fechafin=request.POST['fechafin'],precioviejo=articu.unit_price, articulo=articu)
        ofer.save()
        art.esoferta=True
        articu.unit_price=precionuevo
        articu.save()
        art.save()
        msg="Oferta creada correctamente"
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    else:
        print("Error")
    print("No hace nada")
    return render_to_response('crearoferta.html',{'articulos':productos}, context_instance=RequestContext(request))

@login_required(login_url='home')
def listaroferta(request):
    ofertas=Oferta.objects.all()
    return render_to_response('listaofertas.html',{'ofertas':ofertas}, context_instance=RequestContext(request))

@login_required(login_url='home')
def modoferta(request,oferta_id):
    oferta=get_object_or_404(Oferta,id=oferta_id)
    producto=get_object_or_404(Product,name=oferta.articulo)
    if request.method == 'POST' and 'delete' in request.POST:
        msg=""
        oferta.delete()
        msg="Oferta eliminada correctamente"
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    if request.method == "POST" and 'modify' in request.POST:
        msg=""
        descuento=request.POST['descuento']
        inicio=request.POST['inicio']
        fin=request.POST['fin']
        if descuento != "":
            oferta.descuento=descuento
            final=(int(producto.unit_price)*int(descuento))/100
            precionuevo=int(producto.unit_price)-final
            producto.unit_price=precionuevo
        if inicio != "":
            oferta.fechainicio=inicio
        if fin != "":
            oferta.fechafin=fin
        producto.save()
        oferta.save()
        if descuento !="" or inicio != "" or fin != "":
            msg="Oferta modificada"
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    return render_to_response('modoferta.html',{'oferta':oferta}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def creararticulo(request):
    familias=Familia.objects.all()
    proveedores=Proveedor.objects.all()
    tallas=Talla.objects.all()
    fecha=date.today()
    print(request.POST)
    print("Files",request.FILES)
    if request.method == 'POST' and 'submit' in request.POST:
        prov=Proveedor.objects.get(nombre=request.POST['proveedor'])
        print("Probeedor",prov)
        famili=Familia.objects.get(nombre=request.POST['famili'])
        print("Familia",famili)
        if 'imagen' in request.POST:
            image=request.POST['imagen']
            print(image)
            producto=Product.objects.create(name=request.POST['nombre'], slug=request.POST['slug'], active=1,
                                            date_added=request.POST['fecha'], last_modified=fecha, unit_price=request.POST['precio'])
            producto.save()
            print("Producto Creado")
            print("Date_added",producto.date_added)
            talla=Talla.objects.create(nombre=request.POST['talla'], existencias=request.POST['existencias'])
            talla.save()
            print("Talla creada")
            print(request.POST['devolucion'])
            print(request.POST['imagen'])
            print(prov)
            arti=Articulo.objects.create(product_ptr_id=producto.id,familia=famili,marca=request.POST['marca'],
                                    devolucion=request.POST['devolucion'],imagen=image,proveedor=prov,esoferta=False)
            msg="Articulo creado correctamente"

            arti.save()
            tallas=request.POST.getlist('tallas')
            print("tallas",tallas)
            for elem in tallas:
                arti.tallas.add(elem)
            return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    else:
        print("Error")
    print("No hace nada")
    return render_to_response('creararticulo.html',{'familias':familias,'proveedores':proveedores,'tallas':tallas}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def listararticulo(request):
    articulo=Articulo.objects.all()
    productos=[]
    for elem in articulo:
        prod=get_object_or_404(Product,id=elem.product_ptr_id)
        productos.append(prod)
    return render_to_response('listarticulos.html',{'articulo':articulo,'productos':productos}, context_instance=RequestContext(request))


@login_required(login_url='/home')
def modarticulo(request,articulo_id):
    articulo=get_object_or_404(Articulo,id=articulo_id)
    familias=Familia.objects.all()
    proveedores=Proveedor.objects.all()
    tallas=Talla.objects.all()
    tallasarticulo=Talla.objects.all().filter(articulo=articulo)
    print(request.POST)
    if request.method == 'POST' and 'delete' in request.POST:
        msg=""
        articulo.delete()
        msg="Articulo eliminado"
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    if request.method == 'POST' and 'modify' in request.POST:
        msg=""
        nombre=request.POST['nombre']
        familia=Familia.objects.get(nombre=request.POST['familia'])
        tallas=request.POST.getlist('tallas')
        precio=request.POST['precio']
        marca=request.POST['marca']
        devolucion=request.POST['devolucion']
        proveedor=Proveedor.objects.get(nombre=request.POST['proveedor'])
        for elem1 in articulo.tallas.all():
            articulo.tallas.remove(elem1)
        if 'imagen' in request.POST:
            imagen=request.POST['imagen']
            articulo.imagen=imagen
        if nombre != "":
            articulo.name=nombre
        if familia != "":
            articulo.familia=familia
        if tallas != "":
            for elem in tallas:
                articulo.tallas.add(elem)
        if precio != "":
            articulo.unit_price=precio
        if marca != "":
            articulo.marca=marca
        if devolucion != "":
            articulo.devolucion=devolucion
        if proveedor != "":
            articulo.proveedor=proveedor
        if request.POST['imagen'] != "":
            imagen=request.POST['imagen']
            articulo.imagen=imagen
        else:
            imagen=request.POST['img']
            articulo.imagen=imagen
        articulo.save()
        if nombre!= "" or tallas != "" or familia != "" or precio != "" or marca != "" or devolucion != "" or proveedor != "" or imagen != "":
            msg="Articulo Actualizado"
            print(msg)
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    return render_to_response('modarticulo.html',{'articulo':articulo,'familias':familias,
                                                  'tallas':tallas,
                                                  'tallasarticulo':tallasarticulo,
                                                  'proveedores':proveedores},context_instance=RequestContext(request))

@login_required(login_url='/home')
def crearfamilia(request):
    print(request.method)
    if request.method == 'POST' and "submit" in request.POST:
        familfor= FamiliaForm(request.POST)
        if familfor.is_valid():
            print("dentro del formulario")
            familfor.save()
            print("creacion familia ok")
            msg="Familia creada correctamente"
            return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
        else:
            print("Error")
    print("No hace nada")
    return render_to_response('crearfamilia.html', context_instance=RequestContext(request))

@login_required(login_url='/home')
def listarfamilias(request):
    famili=Familia.objects.all()
    return render_to_response('listafamilias.html',{'famili':famili}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def familia(request, familia_id):
    fam = get_object_or_404(Familia, id=familia_id)
    famili=Familia.objects.all()
    print("Familia antes",famili)
    print(request.POST)
    if request.method == 'POST' and 'delete' in request.POST:
        print("fam",fam)
        fam.delete()
        msg="Familia Eliminada"
        print(msg)
        print("Familia despues",famili)
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    if request.method == 'POST' and 'modify' in request.POST:
        msg=""
        nombre=request.POST['nombre']
        peso=request.POST['pesomedio']
        if nombre != "":
            fam.nombre=nombre
        if peso !="":
            fam.pesomedio=peso
        fam.save()
        if nombre!= "" or peso != "":
            msg="Familia Actualizada"
            print(msg)
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    return render_to_response('modfamilia.html',{'fam':fam}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def listarproveedores(request):
    prov=Proveedor.objects.all()
    return render_to_response('listaproveedores.html',{'prov':prov}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def modproveedor(request, proveedor_id):
    prove=get_object_or_404(Proveedor, id=proveedor_id)
    prov=Proveedor.objects.all()
    print("POST",request.POST)
    if request.method == 'POST' and 'delete' in request.POST:
        prove.delete()
        msg="Proveedor Eliminado"
        return render_to_response('homeadmin.html', {'msg':msg}, context_instance=RequestContext(request))
    if request.method == 'POST' and 'modify' in request.POST:
        nombre=request.POST['nombre']
        msg=""
        direccion=request.POST['direccion']
        contacto=request.POST['contacto']
        if nombre != "":
            prove.nombre=nombre
        if direccion != "":
            prove.direccion=direccion
        if contacto != "":
            prove.contacto=contacto
        prove.save()
        if nombre!= "" or direccion!= "" or contacto!= "":
            msg="Proveedor actualizado"
        return render_to_response('homeadmin.html', {'msg':msg}, context_instance=RequestContext(request))

    return render_to_response('modproveedor.html',{'prove':prove},context_instance=RequestContext(request))

@login_required(login_url='/home')
def listacompania(request):
    companias=Compania.objects.all()
    return render_to_response('listacompanias.html',{'companias':companias}, context_instance=RequestContext(request))

@login_required(login_url='/home')
def modcompania(request,compania_id):
    comp=get_object_or_404(Compania,id=compania_id)
    companias=Compania.objects.all()
    if request.method == 'POST' and 'delete' in request.POST:
        comp.delete()
        msg="Compania Eliminada"
        return render_to_response('homeadmin.html', {'msg':msg}, context_instance=RequestContext(request))
    if request.method == 'POST' and 'modify' in request.POST:
        nombre=request.POST['nombre']
        contacto=request.POST['contacto']
        peso1=request.POST['peso1']
        peso2=request.POST['peso2']
        peso3=request.POST['peso3']
        gastoextra=request.POST['gastoextra']
        if nombre != "":
            comp.nombre=nombre
        if contacto != "":
            comp.contacto=contacto
        if peso1 != "":
            comp.preciopeso1=peso1
        if peso2 != "":
            comp.preciopeso2=peso2
        if peso3 != "":
            comp.preciopeso3=peso3
        if gastoextra != "":
            comp.gastoextra=gastoextra
        comp.save()
        if nombre!= "" or contacto!= "" or peso1 !="" or peso2 !="" or peso3 !="" or gastoextra !="":
            msg="Compania actualizada"
        return render_to_response('homeadmin.html', {'msg':msg}, context_instance=RequestContext(request))

    return render_to_response('modcompania.html',{'comp':comp},context_instance=RequestContext(request))

@login_required(login_url='/home')
def modificacuenta(request):
    cuenta=numerocuenta.objects.all()
    if request.method == 'POST' and 'submit' in request.POST:
        numero=request.POST['cuenta']
        msg=""
        if numero != "":
            cuenta[0].numero=numero
        cuenta[0].save()
        msg="Numero de cuenta modificado"
        return render_to_response('homeadmin.html',{'msg':msg},context_instance=RequestContext(request))
    print(cuenta)
    return render_to_response('modcuenta.html',{'cuenta':cuenta[0]},context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/home")

def categoria(request,familia_id):
    familia=get_object_or_404(Familia,id=familia_id)
    familias=Familia.objects.all()
    articulos_familia=Articulo.objects.filter(familia=familia,esoferta=False)
    print(articulos_familia)
    print("POST",request.POST)
    if request.method == 'POST' and 'carrito' in request.POST:
        objeto=request.POST['idarticulo']
        articulo=get_object_or_404(Articulo,id=objeto)
        lista=request.session['carritodecompra']
        lista.append(articulo)
        request.session['carritodecompra']=lista
    return render_to_response('familia.html',{'familia':familia,'familias':familias,'articulos':articulos_familia},context_instance=RequestContext(request))

@login_required(login_url='/home')
def perfil(request):
    djangouser=request.user
    deportuser=DeporUser.objects.get(djangoUser=djangouser)
    gusto=Gusto.objects.get(deporuser=deportuser)
    return render_to_response('perfil.html',{'user':deportuser,'gusto':gusto},context_instance=RequestContext(request))


@login_required(login_url='/home')
def nuevogusto(request):
    djangouser=request.user
    deportuser=DeporUser.objects.get(djangoUser=djangouser)
    marcas=Marca.objects.all()
    size=len(marcas)
    fecha=date.today()
    gusto=Gusto.objects.get(deporuser=deportuser)
    if request.method == 'POST' and 'submit' in request.POST:
        marcas=request.POST.getlist('marca')
        print("1",marcas)
        print("2",gusto.marca.all())
        for elem in marcas:
            print(elem)
            if elem in gusto.marca.all():
                gusto.marca.remove(elem)
                gusto.marca.add(elem)
            else:
                gusto.marca.add(elem)

        gusto.save()
        return render_to_response('perfil.html',{'user':deportuser,'gusto':gusto},context_instance=RequestContext(request))
    return render_to_response('nuevogusto.html',{'marcas':marcas,'size':size},context_instance=RequestContext(request))


def eliminargusto(request):
    djangouser=request.user
    deportuser=DeporUser.objects.get(djangoUser=djangouser)
    gusto=Gusto.objects.get(deporuser=deportuser)
    if request.method == 'POST' and 'submit' in request.POST:
        marca=request.POST.getlist('marca')
        print(marca)
        for elem in gusto.marca.all():
            if elem.nombre in marca:
                gusto.marca.remove(elem)
        return render_to_response('perfil.html',{'user':deportuser,'gusto':gusto},context_instance=RequestContext(request))
    return render_to_response('eliminagusto.html',{'gusto':gusto},context_instance=RequestContext(request))


def editarperfil(request):
    djangouser=request.user
    deportuser=DeporUser.objects.get(djangoUser=djangouser)
    gusto=Gusto.objects.get(deporuser=deportuser)
    msg=""
    if request.method == 'POST' and 'submit' in request.POST:
        username=request.POST['username']
        email=request.POST['email']
        nacimiento=request.POST['nacimiento']
        poblacion=request.POST['poblacion']
        if username != "":
            deportuser.djangoUser.username=username
        if email != "":
            deportuser.djangoUser.email=email
        if nacimiento != "":
            deportuser.birthday=nacimiento
        if poblacion != "":
            deportuser.poblacion=poblacion
        deportuser.save()
        msg="Datos modificados correctamente"
        return render_to_response('perfil.html',{'user':deportuser,'gusto':gusto,'msg':msg},context_instance=RequestContext(request))
    if request.method == 'POST' and 'delete' in request.POST:
        deportuser.delete()
        djangouser.delete()
        logout(request)
        msg="Cuenta eliminada correctamente"
        return HttpResponseRedirect("/home")
    return render_to_response('editarperfil.html',{'deportuser':deportuser},context_instance=RequestContext(request))



def search(request):
    search_query = request.POST['search']
    print(len(search_query))
    res = Articulo.objects.filter(name__search=search_query)
    return render_to_response('search_result.html', {'res': res}, context_instance=RequestContext(request))
