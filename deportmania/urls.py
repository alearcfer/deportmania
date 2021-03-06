from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from shop import urls as shop_urls
from shop_simplevariations import urls as simplevariations_urls
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deportmania.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^something/paypal/', include('paypal.standard.ipn.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$','deportmania.views.home'),
    url(r'^articulo/(?P<articulo_id>\w+)/$','deportmania.views.articulo', name='articulo_info'),
    url(r'^oferta/(?P<oferta_id>\w+)/$','deportmania.views.oferta', name="ofe_info"),
    url(r'^quienes$','deportmania.views.quienes'),
    url(r'^contacto$','deportmania.views.contacto'),
    url(r'^politica$','deportmania.views.politica'),
    url(r'^familia$','deportmania.views.familia'),
    url(r'^register$','deportmania.views.register'),
    url(r'^terms$','deportmania.views.terminos'),
    url(r'^login$','deportmania.views.logeo'),
    url(r'^homeadmin$','deportmania.views.principaladmin'),
    url(r'^crearfamilia$','deportmania.views.crearfamilia',name='crea_familia'),
    url(r'^listafamilias$','deportmania.views.listarfamilias'),
    url(r'^familia/(?P<familia_id>\w+)/$','deportmania.views.familia', name='familia_info'),
    url(r'^crearproveedor$', 'deportmania.views.crearproveedor'),
    url(r'^crearcompania$','deportmania.views.crearcompania'),
    url(r'^crearoferta$','deportmania.views.crearoferta'),
    url(r'^creararticulo$','deportmania.views.creararticulo'),
    url(r'^listaproveedor$','deportmania.views.listarproveedores'),
    url(r'^proveedor/(?P<proveedor_id>\w+)/$','deportmania.views.modproveedor',name='proveedor_info'),
    url(r'^listacompania$','deportmania.views.listacompania'),
    url(r'^compania/(?P<compania_id>\w+)/$','deportmania.views.modcompania',name='compania_info'),
    url(r'^modificacuenta$','deportmania.views.modificacuenta'),
    url(r'^listarticulo$','deportmania.views.listararticulo'),
    url(r'^modarticulo/(?P<articulo_id>\w+)/$','deportmania.views.modarticulo',name='art_info'),
    url(r'^listaoferta$','deportmania.views.listaroferta'),
    url(r'^modferta/(?P<oferta_id>\w+)/$','deportmania.views.modoferta',name='oferta_info'),
    url(r'^cerrar/$','deportmania.views.logout'),
    url(r'^categoria/(?P<familia_id>\w+)/$','deportmania.views.categoria',name="fami_info"),
    url(r'^ofertas/$','deportmania.views.ofertas'),
    url(r'^nuevogusto/$','deportmania.views.nuevogusto'),
    url(r'^eliminarmarca/$','deportmania.views.eliminargusto'),
    url(r'^editperfil/$','deportmania.views.editarperfil'),
    url(r'^perfil/$','deportmania.views.perfil'),
    url(r'^busqueda/$','deportmania.views.buscaarticulo',name='busqueda'),
    url(r'^ponertalla/$','deportmania.views.ponertalla'),
    url(r'^modificartalla/$','deportmania.views.modificartalla'),
    url(r'^tallainfo/(?P<tallaarticulo_id>\w+)/$','deportmania.views.tallainfo', name="talla_info"),
    url(r'^shop/checkout/gracias/actualizacion$','deportmania.views.actualizacion'),
    url(r'^recomendacion$','deportmania.views.recomendacion'),
    url(r'^pedidos$','deportmania.views.pedidos'),
    url(r'^shop/checkout/gracias/$','deportmania.views.finalizarorder'),
    url(r'^factura/(?P<order_id>\w+)/$','deportmania.views.infofactura',name='factura'),
    url(r'^generafactura$','deportmania.views.factura'),
    url(r'^listausuarios$','deportmania.views.listausuarios'),
    url(r'^usuario/(?P<usuario_id>\w+)/$','deportmania.views.usuarioconcreto',name="usuario_info"),
    url(r'^listapedidos$','deportmania.views.listapedidos'),
    url(r'^pedido/(?P<pedido_id>\w+)/$','deportmania.views.pedidoconcreto',name='pedido_info'),
    url(r'^listado$','deportmania.views.listado'),
    url(r'^comentariosarticulo/(?P<articulo_id>\w+)$','deportmania.views.comentariosarticulo',name='comen_info'),
    url(r'^creartalla$','deportmania.views.creartalla'),
    url(r'^listatalla$','deportmania.views.listatalla'),
    url(r'^modtalla/(?P<talla_id>\w+)/$','deportmania.views.modtalla',name='mod_talla'),
    (r'^shop/cart/', include(simplevariations_urls)),
    (r'^shop/', include(shop_urls)),


)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
