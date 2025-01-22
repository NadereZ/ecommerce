from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
	    verbose_name_plural = 'categories'

   

class Customer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
   

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=300, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uplods/product/', blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name
   

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
	    return f"{self.product}"
    