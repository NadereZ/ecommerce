from django.test import TestCase
from .models import Order
from products.models import Product
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
# Create your tests here.

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='pass1123')
        self.product = Product.objects.create(name='Laptop', price=1000.00)
    
    def test_order_creation(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=1)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.total_price, 1000.00)

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.product = Product.objects.create(name="Laptop", price=1000.00)

    def test_create_order(self):
        url = reverse('order-create')  # Adjust to match your URLs
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['total_price'], 2000.00)
