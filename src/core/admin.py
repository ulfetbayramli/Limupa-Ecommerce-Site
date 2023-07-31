from django.contrib import admin

# Register your models here.
from .models import Subscriber, Contact

admin.site.register(Subscriber)
admin.site.register(Contact)
