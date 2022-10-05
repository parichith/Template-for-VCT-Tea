from .cart import Cart

# This function returns a Cart object
def cart(request):
    return {'cart': Cart(request)}