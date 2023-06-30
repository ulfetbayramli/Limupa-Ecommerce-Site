from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from product.models import Product_version

# Create your models here.

class address_information(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    phone = models.CharField(max_length = 15)
    email = models.EmailField()
    country = models.CharField(max_length = 50, null=True, blank=True)
    province = models.CharField(max_length = 100, null=True, blank=True)
    city = models.CharField(max_length = 100, null=True, blank=True)
    street_addres = models.CharField(max_length = 150)
    is_billing = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name}'s addres information"


    def Meta():
        verbose_name = "Addres infromation"
        verbose_name_plural = "Addres information"



class shipping_addresses(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    country = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=150)
    zip = models.CharField(max_length=10)
     
    def __str__(self):
        return f"{self.first_name}'s shipping address"

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"



class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_wishlist")
    product = models.ManyToManyField(Product_version, related_name="wishlist_product")

    def __str__(self):
        return f"{self.user}'s wishlist"

    def Meta():
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"



class basket_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="basket_item_user")
    product = models.ForeignKey(Product_version,on_delete=models.CASCADE, null=True, blank=True, related_name="basket_item_product")
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return f"{self.user}'s basket item"

    def Meta():
        verbose_name = "basket item"
        verbose_name_plural = "Basket items"

class basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.Case,null=True, blank=True, related_name="user_basket")
    items = models.ManyToManyField(basket_item, related_name="basket_items")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}'s basket"

    def Meta():
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    
class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s order"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    
