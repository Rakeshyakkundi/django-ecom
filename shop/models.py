from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Product(models.Model):
    CATEGORY = (
        ('watch','watch'),
        ('Book','Book'),
        ('Clothes','Clothes'),
        ('Electronic','Electronic')
    )
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100,default=" ")
    publish_date = models.DateTimeField(auto_now_add=True,null=True)
    category = models.CharField(max_length=50,null=True,choices=CATEGORY)
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    u_id=models.AutoField
    name=models.CharField(max_length=50,default="")
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    message=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10,default="")
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500,default="",null=True)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=100)
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return self.update_desc[0:7]+"..."

class ProductComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    time = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)

