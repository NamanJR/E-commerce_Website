from django.db import models
from numpy import product
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Login(models.Model):
    email= models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    def __str__(self):
        return self.category_name

class Sub_Category(models.Model):
    subcatname=models.CharField(max_length=50);
    category=models.ForeignKey(Category,on_delete=models.CASCADE);
    def __str__(self):
        return self.subcatname;

class Product(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default="")
    subcategory= models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=False, default="")
    image=models.ImageField(upload_to="ecommerceimg/productimg")
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    no=models.IntegerField(default=0,null=True)
    sku_id=models.CharField(max_length=100,default=0,null=True )
    def __str__(self):
        return self.name

class Card(models.Model):
    product_id = models.IntegerField()
    

class Buy(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = PhoneNumberField(unique = True, null = False, blank = False)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    product_quantity = models.IntegerField()
    product_price = models.IntegerField(default=0,null=False)
    total = models.IntegerField(default=0,null=False)


