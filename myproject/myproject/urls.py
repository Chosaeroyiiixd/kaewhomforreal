"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import WatchDetailView
from myapp import views
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Watch/<int:pk>', WatchDetailView.as_view(),name='Watch'),
    path('index/', indexView.as_view(),name="index"),
    path('category/', categoryView.as_view(),name='category'),
    path('addtocart-<int:Watch_id>/', addtocartView.as_view(),name='addtocart'),
    path('mycart/', mycartView.as_view(),name='mycart'),
    path('manage-cart/<int:w_id>', managecartView.as_view(),name='managecart'),
    path('search/', searchView.as_view(),name="search"),
    path('register/', customerregistrationView.as_view(), name="customerregistration"),
    path('login', customerloginView.as_view(), name="customerlogin"),
    path('logout/',customerlogoutView.as_view(),name='customerlogout'),
    path('checkout/', checkoutView.as_view(),name="checkout"),
    path('contact/', views.contact,name="contact"),
    path('empty-cart/', emptycartView.as_view(),name="emptycart"),
    path('ordersucess/', ordersuccessView.as_view(),name="ordersuccess"),
    path('profile/', customerprofileView.as_view(), name='profile'),
    path('profile/order-<int:pk>', customerorderdetailView.as_view(), name='orderdetail'),
    path('adminlogin/',AdminLoginView.as_view(), name="adminlogin"),
    path("adminhome/", AdminHomeView.as_view(), name="adminhome"),
    path("adminorder/<int:pk>/", AdminOrderDetailView.as_view(),
         name="adminorderdetail"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/",
         AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),
    
    path("admin-product/list/", AdminProductListView.as_view(),
         name="adminproductlist"),
    path("admin-product/add/", AdminProductCreateView.as_view(),
         name="adminproductcreate"),





]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)