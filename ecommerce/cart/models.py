from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name
    def subtotal(self):
        return self.quantity*self.product.price


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    noofitems=models.IntegerField()
    address=models.TextField()
    phone=models.CharField(max_length=15)
    order_status=models.CharField(default='pending',max_length=20)
    delivery_status=models.CharField(default="pending",max_length=20)
    date_order=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class Account(models.Model):
    accnum=models.CharField(max_length=20)
    acctype=models.CharField(max_length=20)
    amount=models.IntegerField()
    def __str__(self):
        return self.accnum

