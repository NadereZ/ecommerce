from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order
from products.models import Product
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from .serializers import OrderSelializers
from rest_framework.permissions import IsAuthenticated

# Display cart
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    total = items.aggregate(total_price=Sum('product__price'))['total_price'] or 0
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)

# Add item to cart
@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        # Retrieve the product object
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the quantity from the form (default is 1 if not provided)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            return HttpResponseBadRequest("Invalid quantity value.")

        # Check if there's enough stock
        if quantity > product.stock:
            return HttpResponseBadRequest("Not enough stock available.")

        # Get or create a CartItem for the current user
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
        )

        # If the item already exists, update the quantity
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        # Update the product's stock (decrease by the quantity added to the cart)
        product.stock -= quantity
        product.save()

        # Save the cart item
        cart_item.save()

        # Redirect to the cart page or product detail page after adding the item
        return redirect('cart') # Replace with the actual URL name for your cart page

    return redirect('product_detail', pk=product_id) # Redirect for non-POST requests

# Remove item from cart
@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        product = cart_item.product
        cart_item.delete()  # This triggers the signal to restock the product
        messages.success(request, f"{product.name} removed from your cart!")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")

    return redirect('cart_summary')

# Checkout and create order
@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    total = items.aggregate(total_price=Sum('product__price'))['total_price'] or 0
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(user=request.user, total=total)
        for item in items:
            order.products.add(item.product) # Assume ManyToManyField in Order
            item.delete() # Clear cart
        cart.delete() # Clear cart
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

# View order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)

# Orders api
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSelializers
    permission_classes = [IsAuthenticated]
    # Filter orders by the currently authenticated user
    def get_queryset(self):
        return self.get_queryset.filter(user=self.request.user)