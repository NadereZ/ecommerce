from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . serializers import ProductSerializer

# Display all products
def product_list(request):
    category = request.GET.get('category') # Filter by category if specified
    products = Product.objects.all()
    if category:
        products = products.filter(category__name=category)
    context = {
        'products': products,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/product_list.html', context)

# Display product details
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)

# Search for products
def product_search(request):
    query = request.GET.get('q') # Search query from URL
    products = Product.objects.filter(name__icontains=query) if query else []
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/product_search.html', context)
# Homepage View
def home(request):
    return render(request,'home.html')



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]