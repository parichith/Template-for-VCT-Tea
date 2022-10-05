import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from cart.cart import Cart
from orders.models import OrderItem, Order
from .tasks import payment_completed
from shop.models import Product
from shop.recommender import Recommender

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

# The issued described in the comments below were eventually resolved, they
# are included here to show working.

# Update to Redis requires object to go into "products_bought"
# Trying to find a solution to lift the cart product objects into a list, which
# was solved by not returning values from the Order Creation process to this module.

# Testing product updates at 0 indentation level below to line 25:
# yunnan = 'Yunnan'
# afternoon_tea = Product.objects.get(name='Afternoon')
# apple_and_elderflower_tea = Product.objects.get(name='Apple & Elderflower') 
# assam_tea = Product.objects.get(name='Assam')
# yunnan_tea = Product.objects.get(name=yunnan)

# This function processes the payments via the Braintree gateway.  It used to 
# update the recommender until the process refused to work and it was shipped to 
# the Order Creation module.  Print requests and other testing are left in to 
# demonstrate working.
def payment_process(request):
    # everything = request.session.all() - attempt to catch all objects in the payment
    # print(everything) - creates an error
    order_id = request.session.get('order_id')
    print(order_id)
    order = get_object_or_404(Order, id=order_id)
    print(order)

    # total_cost = order.get_total_cost()
    # trying below with comman for two return values, one of which is the cart object list
    # ref: https://note.nkmk.me/en/python-function-return-multiple-values/
    # total_cost, cart_products_list = order.get_total_cost()
    total_cost = order.get_total_cost()

    # The above print commands were used to identify what was being passed to the order
    # print results:
    # 37
    # Order 37

    # The below doesn't run correctly
    # recommender_add_list = order.get_product_name_list()

    # The below two lines works but gets a list of numbers, a long list. It gets the Foreign Key.
    # name = OrderItem.objects.values_list('product', flat=True)
    # print(product)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task - not enabled due to invalid OS
            # payment_completed.delay(order.id)
            # name = list(Product.objects.get(name=OrderItem.objects.get(product=product)))
            # cart_products = [item['product'] for item in cart]

            # Insert Recommender Update Here
            r = Recommender()
            # r.products_bought(cart_products_list)
            # r.products_bought(cart_products)
            # r = Recommender()
            # r.products_bought([afternoon_tea, apple_and_elderflower_tea, assam_tea, yunnan_tea])

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generates a token for payment
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})

# Function returns a payment done pathway
def payment_done(request):
    return render(request, 'payment/done.html')

# Function returns a payment cancelled pathway
def payment_canceled(request):
    return render(request, 'payment/canceled.html')