from django.contrib import admin
from myapp.models import *

class WatchAdmin(admin.ModelAdmin):
    list_display=['id','brand','model','des','price']

class categoryAdmin(admin.ModelAdmin):
    list_display=['id','category']

class contactAdmin(admin.ModelAdmin):
    list_display=['name','surname','email','message']

class orderAdmin(admin.ModelAdmin):
    list_display=['cart','ordered_by','shipping_address','mobile','email','subtotal','paymentcardno','discount','total','order_status','created_at']

class customerAdmin(admin.ModelAdmin):
    list_display = ['id','name','surname','address']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','customer','total','created_at']

class CartwatchAdmin(admin.ModelAdmin):
    list_display = ['id','cart','watch','price','quantity','subtotal']  

class AdminAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','image','mobile'] 
admin.site.register(Watch, WatchAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(order, orderAdmin)
admin.site.register(customer, customerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Cartwatch, CartwatchAdmin)
admin.site.register(contact, contactAdmin)
admin.site.register(Admin, AdminAdmin)

