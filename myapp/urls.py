from unicodedata import name
from xml.sax import handler
from django import views
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings;
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name="index"),
    path('admin_login/',views.admin_login, name="login"),
    path('check/',views.check, name="check"),
    path('dashboard/',views.dashboard, name="admindashboard"),
    path('productdetails', views.details, name="product_details"),
    path('subcat_list', views.subcat_list, name="subcategory_product_view"),
    path("all_subcategory/",views.all_subcategory, name="all_subcategory"),

    # CATEGORY MANAGEMENT
    path('categorymanage/',views.categorymanage,name='categorymanage'),
    path('add/',views.addcat, name='add_category'),
    path('delete',views.cat_delete, name='category_delete'),
    path('edit',views.cat_edit, name='edit_category'),
    path('update/', views.cat_update, name="update"),

    # SUB-CATEGORY MANAGEMENT
    path('submanage/',views.submanage,name='submanage'),
    path('sub_add/',views.add_subcat, name='add_subcategory'),
    path('delete_sub',views.subcat_delete, name='subcategory_delete'),
    path('edit_sub',views.subcat_edit, name='edit_subcategory'),
    path('subupdate/', views.subcat_update, name="update"),

    #PRODUCT
    path('addproduct/',views.addproduct,name='addproduct'),
    path('additem/',views.additem,name="additem"),
    path('deleteproduct/',views.deleteproduct, name='deleteproduct'),
    path('productdata',views.productdata,name='productdata'),

    #CARD
    path('addingitem',views.addingitem,name='addingitem'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('deletecart',views.deletecart,name='deletecart'),

    #CHECKOUT
    path('checkout/',views.checkout,name='checkout'),

    #ORDER
    path('order/',views.order,name='order'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 ="myapp.views.error_404_view"