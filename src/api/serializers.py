from rest_framework import serializers 
from order.models import wishlist, basket, basket_item, order
from product.models import Size, Category, Color, Manufacturer, Product, Product_version 
from users.models import User 

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields=[
            'name'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            # 'id',
            'name',
            'is_main',
            'p_category'
        ]

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            'name'
        ]
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = [ 
            'name'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    manufacturer = ManufacturerSerializer
    detail_url = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'discount_price',
            'in_sale',
            'category',
            'description',
            'manufacturer',
            'detail_url'
        ]
        
    def get_detail_url(self, obj):
        return obj.get_absolute_url()


class ProductVersionSerializer(serializers.ModelSerializer):
    color = ColorSerializer
    product = ProductSerializer
    size = SizeSerializer
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = Product_version
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'read_count', 
            'cover_image',
            'color',
            'product',
            'size',
            'units_sold'
        ]

    def get_product_name(self, obj):    
        return obj.product.name

    def get_product_price(self, obj):
        return obj.product.price