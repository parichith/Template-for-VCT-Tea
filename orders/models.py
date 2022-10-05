from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from coupons.models import Coupon

# This class holds all the details of a particular order, and has a method to calculate
# the cost of one billing list
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self): # the class object Order will idenify itself by its ID
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.discount / Decimal(100))

    # Below are some trial coding attempts for methods which handle product objects which
    # were to be used with the recommender system.

    # The idea was to simulate a kind of global variable without actually using one by allowing
    # the list of products to be manufactured separately whilst the bill was being calculated.

    # This did not work, and a new solution was found.

    # def get_product_name_list(self):
    #     product_name_list = []
    #     for item in self.items.all()
    #         product_name_list.append(item.get_product_name())
    #         return product_name_list

    # def get_product_name_list(self):
    #     product_name_list = list(item.get_product_name() for item in self.items.all())
      
    # def get_product_name_list(self):
        # pass



class OrderItem(models.Model):
    # With "on_delete=models.CASCADE":
    # when the referenced object is deleted, also delete the objects that have references to it
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    # name declared here to be returned and added to the list for recommender
    # name = models.CharField(max_length=200, db_index=True, default='Afternoon')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

        assam_tea = Product.objects.get(name='Assam')

    # These methods and the class below are part of the attempt to create a separate calculation for the 
    # product list in the current billing object.

    # Function to return the name of each product whne iterated
    # def get_product_name(self):
    #     return self.product >>> wrong its a foreign key

    # def get_product_name(self):
    #     product_name_list = []
    #     product_name = Product.objects.get()


# class RecommenderUpdate(models.Model):
#     order = models.ForeignKey(Order,
#                               related_name='items',
#                               on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,
#                                 related_name='order_items',
#                                 on_delete=models.CASCADE)
#     name = models.ForeignKey(Product,
#                                 related_name='order_items',
#                                 on_delete=models.CASCADE)

