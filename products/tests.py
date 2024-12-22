from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Product

# Create your tests here.

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=1000.00,
            category='digital',
            stock=400
        )
        self.assertEqual(product.name, 'Laptop')
        self.assertEqual(product.price, 1000.00)


class ProductAPITest(APITestCase):
    def setUp(self):
        Product.objects.create(name='Laptop', price=1000.00)
        Product.objects.create(name='Phone', price=500.00)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)