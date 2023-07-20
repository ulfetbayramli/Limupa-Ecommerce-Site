from django.db import models
from django.urls import reverse

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""






class Category(models.Model):
    name=models.CharField(max_length=50)
    is_main = models.BooleanField(default=True)
    p_category  = models.ForeignKey("Category", on_delete= models.CASCADE , related_name="parent_category", null=True, blank=True)
    
    def __str__(self):
        return self.name


    def save(self):
        if self.p_category is None:
            self.is_main = True
        else:
            self.is_main = False
        return super().save()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"




class Color(models.Model):
    name=models.CharField(max_length=50 )
    color_code = models.CharField(max_length=100, default="white")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

class Manufacturer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Manufacturer"
        verbose_name_plural = "Product Manufacturers"




class Product(models.Model):
    name = models.CharField(max_length=255)
    in_sale = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category", null=True)
    description = models.TextField(blank=True, help_text='A detailed description of the product, including features, benefits, and specs')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,related_name="product_manufacturer" , null=False, blank=True)
    
    # size = models.ForeignKey(Size, on_delete=models.CASCADE)
    # updated_at = models.DateTimeField(auto_now=True)  
    # image = models.ManyToManyField(Image, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])


class Product_version(models.Model):
    quantity = models.PositiveIntegerField()
    review_count = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='The regular price of the product', default=2000)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='The discounted price of the product')
    date_added = models.DateTimeField(auto_now_add=True)
    read_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="product_images/")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="product_color")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_version")
    images = models.ManyToManyField(Image, related_name='images_of_products')
    size = models.ManyToManyField(Size, blank= True)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT, blank=True, null=True, related_name="product_storage")
    units_sold = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name}'s {self.color.name} version"

    class Meta:
        verbose_name = "Product Version"
        verbose_name_plural = "Product Versions"



class Sale(models.Model):
    product_version = models.ForeignKey(Product_version, on_delete=models.CASCADE)
    units_sold = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_version} - {self.units_sold} units sold on {self.sale_date}"
