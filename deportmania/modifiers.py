__author__ = 'alejandroarciniegafernandez'
import decimal

from shop.cart.cart_modifiers_base import BaseCartModifier
from django.conf import settings

class Fixed7PercentTaxRate(BaseCartModifier):
    """
    This will add 7% of the subtotal of the order to the total.

    It is of course not very useful in the real world, but this is an
    example.
    """

    def get_extra_cart_price_field(self, cart, request):
        taxes = decimal.Decimal('0') * cart.subtotal_price
        to_append = ('Taxes total', taxes)
        return to_append


class FixedShippingCosts(BaseCartModifier):



      def add_extra_cart_price_field(self, cart):
        cart.extra_price_fields.append(
            ('Shipping costs', decimal.Decimal(
                settings.SHOP_SHIPPING_FLAT_RATE)))
        return cart




