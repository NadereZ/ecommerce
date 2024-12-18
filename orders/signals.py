from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem
from products.models import Product

# Signal to update stock when CartItem is saved (added or updated)
@receiver(post_save, sender=CartItem)
def update_stock_on_cart_item_save(sender, instance, created, **kwargs):
    product = instance.product
    if created:
        # Check if enough stock is available when the cart item is created
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity # Reduce stock based on quantity
            product.save() # Save the updated stock
        else:
            print(f"Not enough stock for {product.name} in the cart!")
            # Optionally, handle stock shortage (e.g., raise exception, notify user)
    else:
        # Handle updates to CartItem (e.g., if quantity changes)
        previous_quantity = CartItem.objects.get(id=instance.id).quantity
        if instance.quantity > previous_quantity:
            # Adding more items to the cart, reduce stock
            if product.stock >= (instance.quantity - previous_quantity):
                product.stock -= (instance.quantity - previous_quantity)
                product.save()
            else:
                print(f"Not enough stock for {product.name} in the cart!")
        elif instance.quantity < previous_quantity:
            # Reducing the quantity in the cart, restock
            product.stock += (previous_quantity - instance.quantity)
            product.save()

# Signal to update stock when CartItem is deleted (removed from cart)
@receiver(post_delete, sender=CartItem)
def update_stock_on_cart_item_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity # Restock when CartItem is deleted
    product.save() # Save the updated stock
