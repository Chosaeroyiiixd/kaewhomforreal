from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class category(models.Model):
    category = models.CharField(max_length=30,default=None)

    def __str__(self):
        return "%s"\
            %(self.category)

class customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Watch(models.Model):
    brand=models.CharField(max_length=30)
    model=models.CharField(max_length=30)
    category=models.ForeignKey(category,default=None,related_name='+',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    des = models.CharField(max_length=1000, default=None)
    image=models.ImageField(blank=True,null=True)


    def __str__(self):
        return "brand:%s"\
            %(self.brand)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('Watch', args=[str(self.id)])


class Cart(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Watch,on_delete=models.CASCADE,null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart : ' + str(self.id)

class Cartwatch(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return 'Cart : ' + str(self.cart.id) + 'Cartwatch : ' + str(self.id)

ORDER_STATUS = ( 
    ('Order Received','Order Received'),
    ('Delivering','Delivering'),
    ('Delivered','Delivered'),
    ('Order Canceled', 'Order Canceled'),
)


class order(models.Model):
    cart =  models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    paymentcardno = models.CharField(max_length=15,default=None)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order : " + str(self.id)


class contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=300)
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.name




