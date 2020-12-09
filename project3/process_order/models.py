from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE,default=None)
    order_code =models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    price = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.order_code
    
    def price(self):
        s = 0
        for order_detail in self.order_detail.all():
            s+= order_detail.price()
            
        return s
    
    def check_wrap(self):
        s=0
        nw = 0
        for order_detail in self.order_detail.all():
            s+=order_detail.quality
            nw+=order_detail.quality_wraped
        return s==nw
        
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    product_id = models.CharField(max_length=8,unique=True)
    image_product = models.FileField(upload_to='image_product/',blank=True)
    image_product1 = models.FileField(upload_to='image_product/',blank=True)
    image_product2 = models.FileField(upload_to='image_product/',blank=True)
    image_product3 = models.FileField(upload_to='image_product/',blank=True)
    image_product4 = models.FileField(upload_to='image_product/',blank=True)
    product_quality = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default = 0)
    discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order_detail(models.Model):
    product_id = models.CharField(max_length=8)
    quality = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(Order, related_name='order_detail',on_delete=models.CASCADE)
    quality_wraped = models.PositiveIntegerField(default=0)

    def price(self):
        return Product.objects.get(product_id = self.product_id).price* self.quality

    def getName(self):
        return Product.objects.get(product_id= self.product_id).name





