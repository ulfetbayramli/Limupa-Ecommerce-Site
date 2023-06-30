from django.contrib import admin

# Register your models here.
from .models import address_information, shipping_addresses, wishlist, basket_item, basket, order

admin.site.register(address_information)
admin.site.register(shipping_addresses)
admin.site.register(wishlist)
admin.site.register(basket_item)
admin.site.register(basket)
admin.site.register(order)
