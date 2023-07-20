from django.contrib import admin

# Register your models here.
from .models import Size, Product, Product_version, Category, Color, Image, Manufacturer, Sale, Storage


admin.site.register(Size)
admin.site.register(Storage)
admin.site.register(Image)
admin.site.register(Color)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Product_version)
admin.site.register(Product)
admin.site.register(Sale)
