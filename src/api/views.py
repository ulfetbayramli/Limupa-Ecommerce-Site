from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import ProductSerializer, ProductVersionSerializer

from order.models import wishlist, basket, basket_item, order
from product.models import Size, Category, Color, Manufacturer, Product, Product_version 
from users.models import User 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ProductListAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductVersionListAPi(ListAPIView):
    queryset = Product_version.objects.all()
    serializer_class = ProductVersionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product__category', 'color__name', 'product__manufacturer__name']
    search_fields = ['product__name', 'product__description']
    ordering_fields = ['product__price']