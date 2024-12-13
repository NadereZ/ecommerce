from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller','Seller'),
        ('buyer','Buyer'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return self.get_username
    

class Category(models.Model):
        name = models.CharField(max_length=100)
        description = models.TextField(blank=True, null=True)

        def __str__(self):
            return self.name
        
class Product(models.Model):
        seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'seller'})
        category = models.ForeignKey(on_delete=models.SET_NULL, null=True)
        name = models.CharField(max_length=100)
        description = models.TextField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        stock = models.PositiveIntegerField()
        image = models.ImageField(upload_to=None, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name
        
class Order(models.Model):
        STATUS_CHOICES = [
            ('pending','Pending'),
            ('completed','Completed'),
            ('cancelled','Cancelled'),
        ]
        buyer = models.ForeignKey('CustomUser', on_delete=models.CASCADE,limit_choices_to={'role': 'buyer'})
        products = models.ManyToManyField('Product', through='OrderItem')
        status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
        total_amont = models.DecimalField(max_digits=10, decimal_places=2)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return f"Order {self.id} by {self.buyer.username}"
    

class OrderItem(models.Model):
        order = models.ForeignKey('Order', on_delete=models.CASCADE)
        product = models.ForeignKey('Product', on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)

        def __str__(self):
            return f"{self.quantity} of {self.product.name} in Order {self.order.id}"
        
class Payment(models.Model):
        order = models.OneToOneField('Order', on_delete=models.CASCADE)
        payment_method = models.CharField(max_length=50)
        payment_status = models.CharField(max_length=50, default='pending')
        transaction_id = models.CharField(max_length=100, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Payment for order {self.order.id}"


class Review(models.Model):
      buyer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
      product = models.ForeignKey('Product', on_delete=models.CASCADE)
      rating = models.PositiveIntegerField()
      comment = models.TextField(blank=True, null=True)
      created_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f"Review by {self.buyer.username} for {self.product.name}"