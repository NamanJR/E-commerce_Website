from distutils.command.upload import upload
from email.mime import image
from itertools import product
from multiprocessing import context
import re
from unicodedata import category, name
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Card, Login
from .models import Category
from .models import Sub_Category
from . models import Product
from . models import Buy


# Create your views here.
def index(request):
    category=Category.objects.all()
    product=Product.objects.all()
    subid=request.GET.get("subcatid")
    carddata= Card.objects.all()
    card_data=len(carddata)
    if subid:
        product=Product.objects.filter(subcategory=subid)
    else:
        product=Product.objects.all()
    context={
        'categorydata':category,
        'productdata':product,
        "card":card_data
    }
    return render(request,"index.html",context)

def admin_login(request):
    return render(request,"Admin/admin_login.html")

def check(request):
    if(request.method=="POST"):
        uemail=request.POST.get("uemail")
        upass=request.POST.get("upass")
        data = Login.objects.filter(email=uemail,password=upass)
        if(len(data)>0):
            return render(request,"admin/dashboard.html")
        else:
            return redirect("admin_login")

def dashboard(request):
    return redirect("admin/dashboard")

def details(request):
    category=Category.objects.all()
    detail_id= request.GET.get("details_id")
    product_id=Product.objects.filter(id=detail_id)
    context={
        'categorydata':category,
        'product_data':product_id
    }
    return render(request,"productdetails.html",context)

def subcat_list(request):
    subcat_id=request.GET.get("subcatid")
    subcat=Product.objects.filter(subcategory=subcat_id)
    category=Category.objects.all()
    context={
        'categorydata':category,
        "subcategorylist":subcat

    }
    return render(request,"all_subcategory.html",context)

def all_subcategory(request):
    return render(request,"all_subcategory.html")

def error_404_view(request,exception):
    return render(request,"pagenotfound.html",status=404)

#----------------------------------------------Category_Management-----------------------------------------

def categorymanage(request):
    categories=Category.objects.all()
    return render(request,'admin/categorymanage.html',{"category":categories})

def addcat(request):
    if(request.method=="POST"):
        cat_data= request.POST.get("cat")
        cat_added=Category(category_name=cat_data)
        cat_added.save()
        return redirect ('categorymanage')

def cat_delete(request):
    cat_data = request.GET.get("uid")
    Category.objects.filter(id=cat_data).delete()
    return redirect ('categorymanage')

def cat_edit(request):
    cat_data = request.GET.get("uid")
    edit_data=Category.objects.filter(id=cat_data)
    return render(request,'admin/update.html',{"edit":edit_data})

def cat_update(request):
    if(request.method=="POST"):
        cat_id= request.POST.get('userid')
        data= request.POST.get('uname')
        Category.objects.filter(id=cat_id).update(category_name=data)
        return redirect('categorymanage')


#------------------------------------------------- SUB-CATEGORY----------------------------------------------

def submanage(request):
    sub_cat=Sub_Category.objects.all()
    main_cat=Category.objects.all()
    context ={
        "categories" :sub_cat,
        "main_categories":main_cat
    }
    return render(request,'admin/submanage.html',context)

def add_subcat(request):
    if(request.method=="POST"):
        cat_data = request.POST.get("data")
        sub_data= request.POST.get("cat")
        information=Sub_Category(subcatname=sub_data,category=Category.objects.filter(category_name=cat_data).first())
        information.save();
        return redirect ('submanage')

def subcat_delete(request):
    cat_data = request.GET.get("uid")
    Sub_Category.objects.filter(id=cat_data).delete()
    return redirect('submanage')

def subcat_edit(request):
    cat_data = request.GET.get("uid")
    edit_data=Sub_Category.objects.filter(id=cat_data)
    return render(request,'admin/subupdate.html',{"edit":edit_data})

def subcat_update(request):
    if(request.method=="POST"):
        cat_id= request.POST.get('userid')
        data= request.POST.get('uname')
        Sub_Category.objects.filter(id=cat_id).update(subcatname=data)
        return redirect('submanage')

#------------------------------------------------Product------------------------------------------

def addproduct(request):
    category=Category.objects.all()
    subcategory=Sub_Category.objects.all()
    context={
        "category": category,
        "subcategory":subcategory
    }
    return render(request ,"admin/addproduct.html",context)

def additem(request):
    if request.method=="POST" and request.FILES['upload']:
        upload=request.FILES['upload']
        pname=request.POST.get('pname')
        pquantity=request.POST.get('pquantity')
        pprice=request.POST.get('pprice')
        pskuid=request.POST.get("pskuid")
        pcat=request.POST.get("cat")
        psubcat=request.POST.get("subcat")
        data=Product(category=Category.objects.filter(category_name=pcat).first(),subcategory=Sub_Category.objects.filter(subcatname=psubcat).first(),image=upload,name=pname,price=pprice,no=pquantity,sku_id=pskuid)
        data.save()
        return redirect('addproduct')

def deleteproduct(request):
    productdata= Product.objects.all()
    return render(request,"admin/viewproduct.html",{"product":productdata})

def productdata(request):
    product_id=request.GET.get('details_id')
    Product.objects.filter(id=product_id).delete()
    return redirect ('deleteproduct')


#-----------------------------------------------CARD---------------------------------------------------

def addingitem(request):
    p_id=request.GET.get('items')
    data=Card.objects.filter(product_id=p_id)
    if len(data)>0:
        return redirect('index')
    else:
        card = Card(product_id=p_id)
        card.save()
        return redirect('index')

def addtocart(request):
    card_data = Card.objects.values_list('product_id', flat=True)
    data_list=[]
    for data in card_data:
        data_table = Product.objects.filter(id=data)
        data_list.append(data_table)    
    len_count = len(data_list)

    context={
        "product_data":data_list,
        "count_data":len_count 
    }
    return render(request,'addtocart.html',context)

def deletecart(request):
    cart_id= request.GET.get('details_id')
    data = Card.objects.filter(product_id = cart_id).delete()
    return redirect('addtocart')

#-----------------------------------------CHECKOUT--------------------------------------------------------------

def checkout(request):
    if(request.method == "POST"):
        pquantity = request.POST.getlist("quantity");
        pname = request.POST.getlist("pname");
        pprice=request.POST.getlist("price");
        ptotal=request.POST.get("total")
        
        context={
            "name":pname,
            "quantity":pquantity,
            "price":pprice,
            "total":ptotal
        }
        return render(request,"checkout.html",context)

#----------------------------------------------ORDER-----------------------------------------------------------------

def order(request):
    if request.method=='POST':
        uname = request.POST.get("name")
        uemail = request.POST.get('email')
        uphone = request.POST.get('phone')
        ustate = request.POST.get('state')
        ucity = request.POST.get('city')
        uaddress = request.POST.get('address')
        uzip = request.POST.get('zip')
        product = request.POST.getlist("pname")
        product_quantity = request.POST.getlist("pquantity")
        product_price = request.POST.getlist("pprice")
        total = request.POST.get('total')
        print(uname,uemail,uaddress,ucity,ustate,uzip,uphone,product ,product_quantity,product_price)
        return HttpResponse("hi")
