__author__ = 'alejandroarciniegafernandez'

# -*- coding: utf-8 -*-
"""Shipping backend that skips the whole shipping process."""

from decimal import Decimal
from django.conf import settings
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from shop.util.decorators import on_method, shop_login_required, order_required


class SkipShippingBackend(object):

    backend_name = "Skip Shipping Backend"
    url_namespace = "skip-shipping"

    def __init__(self, shop):
        self.shop = shop

    def simple_view(self, request):
        """
        This simple view does nothing but forward to the final URL. When the
        money is sent, the shop owner can set this order to complete manually.
        """
        order = self.shop.get_order(request)
        return self.shop.finished(order)

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.simple_view, name='skip-shipping' ),
        )
        return urlpatterns


class FlatRateShipping(object):
    url_namespace = 'flat'
    backend_name = 'Flat rate'
    backend_verbose_name = _('Flat rate')
    def __init__(self, shop):
        self.shop = shop # This is the shop reference, it allows this backend
    # to interact with it in a tidy way (look ma', no imports!)
        self.rate = getattr(settings, 'SHOP_SHIPPING_FLAT_RATE', '10')

    @on_method(shop_login_required)
    @on_method(order_required)
    def view_process_order(self, request):
        self.shop.add_shipping_costs(self.shop.get_order(request),
                                                'Flat shipping',
                                            Decimal(self.rate))
        return self.shop.finished(self.shop.get_order(request))
    # That's an HttpResponseRedirect
    @on_method(shop_login_required)
    @on_method(order_required)
    def view_display_fees(self, request):
        ctx = {}
        ctx.update({'shipping_costs': Decimal(self.rate)})
        return render_to_response('shop/shipping/flat_rate/display_fees.html',
            ctx, context_instance=RequestContext(request))

    def get_urls(self):

        urlpatterns = patterns('',
        url(r'^$', self.view_display_fees, name='flat'),
        url(r'^process/$', self.view_process_order, name='flat_process'),
        )
        return urlpatterns



