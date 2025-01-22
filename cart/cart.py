from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        
        # Get the current session key if it exists
        cart = self.session.get('session_key', {})
        
        # If there is no session key (new user), create one
        if 'session_key' not in request.session:
            self.session['session_key'] = {}
        
        # Make cart available on all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            # Update quantity if the product already exists in the cart
            self.cart[product_id]['quantity'] += quantity
        else:
            # Add new product to the cart
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': quantity
            }
        
        # Mark the session as modified to ensure it gets saved
        self.session.modified = True

    def __len__(self):
        # Calculate the total number of items in the cart
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

