from django.contrib import admin
from . models import Login
from . models import Category
from . models import Sub_Category
from . models import Product
from . models import Card
from . models import Buy

# Register your models here.
admin.site.register(Login)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Card)
admin.site.register(Buy)



