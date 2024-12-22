from django.core.cache import cache
from .models import Product

def get_product():
    products = cache.get('products')
    if not products:
        products = Product.objects.all()
        cache.set('products', products, 300)
    return products