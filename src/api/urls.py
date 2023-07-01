from django.urls import path
from . import views
from .views import ProductListAPI, ProductVersionListAPi

urlpatterns = [
    path('products', ProductListAPI.as_view(), name='product_detail'),
    path('productversions', ProductVersionListAPi.as_view(), name='product_detail'),
]