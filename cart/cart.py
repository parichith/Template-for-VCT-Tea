from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


# Creates the Cart object.  It uses the session middleware to store the cart with the items from the database.
# Its behaviours are that of your standard shopping cart, and this enabled its management.
class Cart(object):

    # This init function sends the request for a new session to start, self allow other methods to access it.
    def __init__(self, request):
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    # this iterration function allows going through the card to identify all product objects within
    def __iter__(self):

        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # This function counts the number of product objects in the cart
    def __len__(self):

        return sum(item['quantity'] for item in self.cart.values())

    # This adds a product to the cart or updates the amount.
    # It uses the ID of the product as a dictionary key with the price and quanity as values
    def add(self, product, quantity=1, override_quantity=False):

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    # This function removes a product from the cart
    def remove(self, product):

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # This calculates the total price for all objects in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

# Coupons for discount section as an improvement in production value

    # This function searches for a coupon created in django admin, the following functions
    # calculate change in price after it is successfulling implemented.
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    #  This function calculates the discount from a coupon
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    # This function calculates the final price of the product after discount
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
